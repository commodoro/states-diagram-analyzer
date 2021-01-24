from math import log2, ceil
from typing import List


def n_biestables(states: int) -> int:
    return ceil(log2(states))


def asignar_valor_estado(S: int, q_n: int, e_n: int = 0) -> List[int]:
    k = 2**q_n

    def one(n):
        return 1 if n > 0 else 0
    return [one(i & k) for i in range(S) for _ in range(2**e_n)]


def strbin2num(S: str) -> int:
    return sum(int(S[len(S)-1-i])*2**i for i in range(len(S)))


def leer_nodo(S: str) -> List[int]:
    return [int(S[0:S.find('[')]),
            strbin2num(S[S.find('[')+1:S.find(']')]),
            int(S[S.find(']')+1:])]


def listar_nodos() -> List[List[int]]:
    out = []
    with open('./trans.nodes', 'r') as f:
        while line := f.readline():
            out.append(leer_nodo(line))
    return out


def leer_estado(S: str) -> List[int]:
    n, s = S.split(':')
    return [int(n), [int(c) for c in s.rstrip()]]


def listar_estados() -> List[list]:
    out = []
    with open('./states.nodes', 'r') as f:
        while line := f.readline():
            out.append(leer_estado(line))
    return out


if __name__ == "__main__":
    S = int(input("Introduzca el número de estados: "))
    e_n = int(input("Introduzca el número de entradas: "))
    z_n = int(input("Introduzca el número de salidas: "))
    q_n = n_biestables(S)
    print("El numero de biestables será:", q_n)

    Q = [asignar_valor_estado(S, i, e_n) for i in range(q_n)]
    E = [asignar_valor_estado(2**e_n, i)*S for i in range(e_n)]
    Q_next = [['x']*S*2**e_n for i in range(q_n)]
    Z = [['x']*S*2**e_n for i in range(z_n)]

    # Actualizar Q_next
    for nodo in listar_nodos():
        i = 2**e_n*nodo[0]+nodo[1]
        j = 2**e_n*nodo[2]
        for qi in range(q_n):
            Q_next[qi][i] = Q[qi][j]

    # Añadir las salidas
    for s, z in listar_estados():
        for i in range(z_n):
            for j in range(2**e_n):
                Z[i][s*2**e_n+j] = z[i]

    print("Tabla de estados - biestables:")
    # Cabecera
    print(end="\t")
    for i in range(q_n-1, -1, -1):
        print(f"Q{i}", end="\t")
    for i in range(e_n-1, -1, -1):
        print(f"X{i}", end="\t")
    for i in range(q_n-1, -1, -1):
        print(f"Q'{i}", end="\t")
    for i in range(z_n-1, -1, -1):
        print(f"Z{i}", end="\t")

    # Cuerpo Tabla
    print()
    for i in range(S):
        for c in range(2**e_n):
            if c == 0:
                print(f"S{i}", end='\t')
            else:
                print(" ", end='\t')
            for v in Q[::-1]:
                print(v[2**e_n*i+c], end='\t')
            for e in E[::-1]:
                print(e[2**e_n*i+c], end='\t')
            for v in Q_next[::-1]:
                print(v[2**e_n*i+c], end='\t')
            for v in Z[::-1]:
                print(v[2**e_n*i+c], end='\t')
            print()

    # Imprimir Ecuaciones:
    for i, F in enumerate(Q_next):
        print(f"D{i} =", end=" ")
        out = []
        for j in range(S*2**e_n):
            if F[j] == 1:
                out.append("")
                for k, q in enumerate(Q):
                    if q[j] == 1:
                        out[-1] += f"Q{k}"
                    else:
                        out[-1] += f"'Q{k}"
                for k, x in enumerate(E):
                    if x[j] == 1:
                        out[-1] += f"X{k}"
                    else:
                        out[-1] += f"'X{k}"
        print("+".join(out))
