#!/bin/env python3

"""此代码为用RHF方法计算HE能量的RHF方法演示程序。
用RHF方法计算HE的手动计算流程 Quantum Chemistry 5th, P431 EXAMPLE.
"""
import numpy
import math

def OverlapInt(a, b):
    """
        This function use to compute overlap matrix element, and return
        overlap Matrix

        a, b is STO parameter.
    """
    S =[[0,0],[0,0]]
    S[0][0] = 1
    S[1][1] = 1
    S[0][1] = 8 * numpy.sqrt( a**3 * b**3) / (a + b)**3
    S[1][0] = 8 * numpy.sqrt( a**3 * b**3) / (a + b)**3
    
    return S

def Orthogonal( m ):
    """
        this function use to compute the orthogonal matrix S(1/2)
    """
    # compute inverse matrix of overlap matrix
    m = numpy.matrix(m)
    inverS = m.I
    # compute the eigenvalue and eigenvector of the matrix 'inverS'
    # tmp = numpy.dual.eig(inverS)
    [eigValue, eigVector]= numpy.dual.eig(m)

    eigValueMatrix = numpy.matrix(str(eigValue[0]) + ',0; 0,' + str(eigValue[1]))
    b = eigVector * numpy.sqrt(eigValueMatrix) * eigVector.I
    
    # the root of overlap matrix
    return b

def Hamiltonian(a, b):
    """
        compute one electric integral.
    """
    H = [
            [0, 0],
            [0, 0]
            ]
    H[0][0] = 1/2 * a**2 - 2 * a
    H[1][1] = 1/2 * b**2 - 2 * b
    H[0][1] = H[1][0] = numpy.sqrt(a**3 * b**3) * (4 * a * b - 8 * (a + b)) / (a + b)**3

    return H

def DoubleInt(a, b):
    """
        compute double electric integral.
    """
    D = [
            [#0
                [#00
                    [#000
                        0, 0 #0000, 0001
                    ],
                    [#001
                        0, 0 #0010, 0011
                    ]
                ],
                [#01
                    [#010
                        0, 0 #0100, 0101
                    ],
                    [#011
                        0, 0 #0110, 0111
                    ]
                ],
            ],
            [#1 
                [#10
                    [#100
                        0, 0 #1000, 1001
                    ],
                    [#101
                        0, 0 #1010, 1011
                    ]
                ],
                [#11
                    [#110
                        0, 0 #1100, 1101
                    ],
                    [#111
                        0, 0 #1110, 1111
                    ]
                ]
            ]
        ]
    D[0][0][0][0] = 5 * a / 8
    D[1][1][1][1] = 5 * b / 8
    D[0][0][1][1] = D[1][1][0][0] = (a**4 * b + 4*a**3 * b**2 + \
                                    a * b**4 + 4*a**2 * b**3) / (a + b)**4
    D[0][1][0][1] = D[1][0][0][1] = D[0][1][1][0] = D[1][0][1][0] = \
        20 * (a*b)**3 / (a + b)**5
    D[0][0][0][1] = D[0][0][1][0] = D[0][1][0][0] = D[1][0][0][0] = \
        16 * numpy.sqrt(a**9 * b**3) / (3*a + b)**4 * ( (12*a + 8*b)/(a + b)**2 \
        + (9*a + b)/ (2*a**2) )
    D[0][1][1][1] = D[1][1][0][1] = D[1][0][1][1] = D[1][1][1][0] = \
        16 * numpy.sqrt(b**9 * a**3) / (3*b + a)**4 * ( (12*b + 8*a)/(b + a)**2 \
        + (9*b + a)/ (2*b**2) )

    return D

def GuessMoCoef( guess ):
    """
        guess the molecular orbital coefficient.
    """
    MoCoeff = [
                [0, 0],
                [0, 0]
                ]
    k = 2
    m21 = 1 / numpy.sqrt(1 + k**2 + 2*k*guess[0][1])
    m11 = k * m21

    MoCoeff[0][0] = m11
    MoCoeff[1][0] = m21

    print("guess molecular orbital coeff:\n", MoCoeff)
    return MoCoeff

def initDensityM(initGuess):
    """
        compute the initial density matrix from guess MoCoef
    """
    P = [
            [0.9582, 0.2396],
            [0.4792, 0.4791]
        ]
    P[0][0] = 2 * initGuess[0][0] * initGuess[0][0]
    P[0][1] = P[1][0] = 2 * initGuess[0][0] * initGuess[1][0]
    P[1][1] = 2 * initGuess[1][0] * initGuess[1][0]

    print("Guess density matrix:\n", P, end='\n\n')
    return P

def Fock(H, P, D):
    """
        compute Fock Matrix Element
    """
    n = 2
    F = [
            [0, 0],
            [0, 0]
        ]
    for r in range(0,n):
        for s in range(0, n):
            F[r][s] = H[r][s]
            for t in range(0, n):
                for u in range(0, n):
                    F[r][s] += P[t][u] * ( D[r][s][t][u] - 0.5 * D[r][u][t][s] )

    print("Fock Matrix:\n", F, end='\n\n')
    return F


def ComputeVecVal(Fock, T):
    """
        compute the eigenValue(energy) and eigenVector of Fock.
    """
    Fi = T.T * Fock * T
    F = [eigValue, eigVector] = numpy.dual.eig(Fi)

    print("The eigValue of Fock:\n", eigValue)
    print("The eigVector of Fock:\n", eigVector, end='\n\n')
    return F

def FormDensigy(C, T):
    """
        compute new density matrix by the eigenvector of Fock
    """
    
    # compute molecular coeffcient by the eigenvector of Fock and sqrt(S)
    CC = T * C

    CC = [[CC[0,0],CC[0,1]],[CC[1,0],CC[1,1]]]
    # generate new density matrix
    P = initDensityM(CC)

    return P

def isConvege(old, new):
    """
        compare new density matrix and old density matrix.
    """
    n = 2
    crit = 1.0E-7
    delta = 0

    for i in range(0, n):
        for j in range(0, n):
            delta += abs(new[i][j] - old[i][j])

    delta = numpy.sqrt(delta/4)
    print("The delta Density Matrix:\n", delta, end='\n\n')
    if delta < crit:
        # if the delta little than  crit, it's say that the 
        # density matrix is conveged and the loop would terminal
        return False
    else:
        return True

def VNN(distance, electronic):
    """
        Compute the nuclear-repulsion.

        distance        the distance between two atom nuclear.
        electronic      the index of atom.

    """
    e = 1.602117E-19
    vacumm = 8.8541878E-12
    e1 = math.sqrt(e / (4*math.pi*vacumm))

    Z1 = Z2 = 1
    r12 = 1

    Vnn = Z1 * Z2 * e1**2 / r12 

    print("The Nuclear repulsion is:\t{}".format(0))
    return 0

def computEnergy(P, F, H, V):
    """
        compute Hartree-Fock energy.
    """
    n = 2

    EHF = 0
    for i in range(0, n):
        for j in range(0, n):
            EHF += P[i][j] * (F[i][j] + H[i][j])

    EHF *= 0.5 
    EHF += V

    print("The SCF Energy is:\tE(HF)=\t{} Hartrees".format(EHF))

def FinalOUTPUT(P, F, H, V):
    """
        output the final scf energy and so on.
    """

    print("FINAL".center(70, '*'))
    computEnergy(P, F, H, V)

if __name__ == "__main__":
    """
    """
    a1 = 1.45
    a2 = 2.91
    i = 0
    eigVector = 0
    iF = 0

    S = OverlapInt(a1, a2)
    Ss = Orthogonal(S)
    H = Hamiltonian(a1, a2)
    imocoef = GuessMoCoef(S)
    P = initDensityM(imocoef)
    D = DoubleInt(a1, a2)

    PP = [[0,0],[0,0]]
    while isConvege(P, PP):
        # SCF iteration

        print("Iteration:  {}".format(i))
        i += 1

        P = PP
        F = Fock(H, PP, D)
        [eigVector, iF] = ComputeVecVal(F, Ss.I)
        PP = FormDensigy(iF, Ss.I)
    # compute the nuclear repulsion.
    V = VNN(1,1)
    # Output Result.
    FinalOUTPUT(PP, F, H, V)
