
#programa interativo para cálculo de reforço estrutural com concreto textil em vigas de concreto armado
import math


print("=" * 70)
print('''CÁLCULO DE REFORÇO COM CONCRETO TÊXTIL - VIGA SUBMETIDA À FLEXÃO
UNIVERSIDADE FEDERAL DE SERGIPE
Aluna: Agatha Ferreira Oliveira     Orientador: Emerson Figueiredo''')
print("=" * 70)

def dados_de_entrada():
    while True:

        # ---- COLETA DOS DADOS ----
        bw = float(input('Digite a largura da viga (bw) em cm: '))
        h = float(input('Digite a altura da viga (h) em cm: '))
        d = float(input('Digite a distância do centro geométrico da armadura tracionada até a borda mais comprimida (d) em cm: '))
        dc = float(input( 'Digite a distância do centro geométrico da armadura comprimida até a borda mais comprimida (d) em cm: '))
        Ec = float(input('Digite o módulo de elasticidade do concreto (Ec) em GPa: '))
        As = float(input('Digite a área de aço da armadura tracionada (As) em cm²: '))
        Asc = float(input('Digite a área de aço da armadura comprimida (Asc) em cm²: '))
        #Ms = float(input('Digite o momento fletor que a viga deve resistir (Ms) em kN·cm: '))
        Es = float(input('Digite o módulo de elasticidade do aço (Es) em GPa: '))
        l = float (input('Digite a largura entre os apoios da viga (em cm)'))


        # ---- MOSTRAR DADOS DIGITADOS ----
        print("=" * 50)
        print("DADOS DE ENTRADA")
        print("=" * 50)
        print(f"bw  = {bw} cm")
        print(f"h   = {h} cm")
        print(f"d   = {d} cm")
        print(f"dc   = {dc} cm")
        print(f"Ec = {Ec} GPa")
        print(f"As  = {As} cm²")
        print(f"Asc = {Asc} cm²")
        print(f"Es = {Es} GPa")

        # ---- VERIFICAÇÃO ----
        confirma = input("\nOs dados estão corretos? (s/n): ").lower().strip()

        if confirma.startswith('s'):
            return bw, h, d, dc, Ec, As, Asc, Es,l

        else:
            print("\n🔄 Refaça a entrada dos dados...\n")

# --- DADOS REFORÇO TÊXIL --- #
def escolher_têxtil():

    while True:
        print("=" * 50)
        print("DADOS DO REFORÇO TÊXTIL")
        print("=" * 50)

        print('[1] Armo-mesh L500 da S&P')
        print('[2]  AF - 0200 BR  da FiberTEX')
        print('[3] Outro')
        op = int(input('Escolha a opção de têxtil para o reforço: '))

        if op == 1:
            print("Você escolheu a Armo-mesh L500 da S&P")
            return 240, 0.147, 800,0.3,0.0117,"Armo-mesh L500 da S&P"  # Ef, Af1 , σf, ea,et

        elif op == 2:
            print("Você escolheu a AF - 0200 BR da FiberTEX")
            return 70, 0.003269,220, 0.2,0.05,"AF - 0200 BR da FiberTEX" # Ef, Af1, σf, ea,et

        elif op == 3:
            nome = input("Digite o nome do têxtil: ")
            Ef = float(input('Digite o módulo de elasticidade do têxti em GPa:'))
            Af1 = float(input('Digite a área do textil para uma camada em cm:'))
            σf = float(input(' Digite a tensão de escoamento do têxtil em MPa:'))
            ea = float(input('Digite a espessura da argamassa em cm:'))
            et = float(input(' Digite a espessura do têxtil em MPa:'))
            return Ef, Af1, σf,ea,et,nome


        else:
            print("Opção inválida!")
            continue


# --- DIMENSIONAMENTO DO REFORÇO --- #
def dimensionar_reforço(bw, h, d, dc, Ec, As, Asc, Es,l,Ef, Af1, σf,ea,et,nome):
    camadas = 1

    while True:
        # ---Cálculo da Linha Neutra---#
        #df = h + 2*ea + 1.5*et ## Confirmar com professor
        df = h
        Af = Af1 * camadas *bw
        a = (1/2)*Ec*bw
        b = (Es * (As + Asc)) + (Af * Ef)
        c = - ((Es * As * d) + (Asc * dc* Es) + (Af * Ef * df))

        x= (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)

        # --- Cálculo do Momento de Inércia---#
        Ix = (bw * x ** 3) / 3 + (Es / Ec) * As * (d - x) ** 2 + (Es / Ec) * Asc * (x - dc) ** 2 + (Ef / Ec) * Af * (df - x) ** 2

        # --- Cálculo do Momento Resistente---#
        Mr = (Ec/Ef)*(((σf/10)*Ix)/(df-x))
        P = (Mr * 6) / l
        return x, Ix, Mr, camadas, P

        if Mr > Ms:
            return x,Ix,Mr, camadas
        else:
            camadas+=1


def main():
    bw, h, d, dc, Ec, As, Asc, Es,l = dados_de_entrada()
    Ef, Af1, σf, ea, et,nome = escolher_têxtil()
    x, Ix, Mr, camadas, P = dimensionar_reforço(bw, h, d, dc, Ec, As, Asc, Es,l,Ef, Af1, σf,ea,et,nome)


    print("=" * 50)
    print("RESULTADOS")
    print("=" * 50)
    print(f"Posição da linha neutra (x) = {x:.3f} cm")
    print(f"Momento de Inercia (Ix) = {Ix:.3f} cm^4n")
    print(f"Momento Resistente (Mr) = {Mr:.3f} Kn.cm")
    print(f"Carga  (P) = {P:.3f} Kn")
    print(f" O reforço necessário é de {camadas} camadas do concreto têxtil {nome}.")
    print("Programa finalizado!")

if __name__ == "__main__":
    main()

