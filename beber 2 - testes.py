#programa interativo para cálculo de reforço estrutural com concreto textil em vigas de concreto armado
#Análise do ELU


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
        Ec = float(input('Digite o módulo de elasticidade do concreto (Ec) em MPa: '))
        As = float(input('Digite a área de aço da armadura tracionada (As) em cm²: '))
        Asc = float(input('Digite a área de aço da armadura comprimida (Asc) em cm²: '))
        Es = float(input('Digite o módulo de elasticidade do aço (Es) em MPa: '))
        fy = float(input('Digite a tensão de escoamento na armadura tracionada (em MPa): '))
        fyc = float(input('Digite a tensão de escoamento na armadura comprimida (em MPa): '))
        fck = float(input('Digite a resistência característica do concreto (fck) (em MPa): '))
        l = float(input('Digite o vão da viga (em cm): '))

        # ---- MOSTRAR DADOS DIGITADOS ----
        print("=" * 50)
        print("DADOS DE ENTRADA")
        print("=" * 50)
        print(f"bw  = {bw} cm")
        print(f"h   = {h} cm")
        print(f"d   = {d} cm")
        print(f"dc   = {dc} cm")
        print(f"Ec = {Ec} MPa")
        print(f"As  = {As} cm²")
        print(f"Asc = {Asc} cm²")
        print(f"Es = {Es} MPa")
        print(f"fy = {fy} MPa")
        print(f"fyc = {fyc} MPa")
        print(f"fck = {fck} MPa")

        # ---- VERIFICAÇÃO ----
        confirma = input("\nOs dados estão corretos? (s/n): ").lower().strip()

        if confirma.startswith('s'):
            return bw, h, d, dc, Ec, As, Asc, Es, fy, fyc, fck,l

        else:
            print("\n🔄 Refaça a entrada dos dados...\n")


# --- DADOS REFORÇO TÊXIL --- #
def escolher_textil():

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
            return  240000, 0.0105, 4300,0.3,0.0105,"Armo-mesh L500 da S&P"  # Ef, Af1p/cm , Ff , ea,et

        elif op == 2:
            print("Você escolheu a AF - 0200 BR da FiberTEX")
            return 70000, 0.003269, 1000, 0.2,0.05,"AF - 0200 BR da FiberTEX" # Ef, Af1, ff, ea,et

        elif op == 3:
            nome = input("Digite o nome do têxtil: ")
            Ef = float(input('Digite o módulo de elasticidade do têxtil em MPa:'))
            g = float(input('Digite a gramatura da fibra na direção principal em g/m2'))
            p = float(input('Digite a densidade da fibra em g/cm3'))
            Af1 = ((g / 10000) / p)  # Af1/cm em (cm2/cm)
            ff = float(input(' Digite a tensão de escoamento do têxtil em MPa:'))
            ea = float(input('Digite a espessura da argamassa em cm:'))
            et = float(input(' Digite a espessura do têxtil em cm:'))
            return Ef, Af1, ff, ea, et, nome


        else:
            print("Opção inválida!")
            continue

# --- DIMENSIONAMENTO DO REFORÇO --- #


def dimensionar_reforco(bw, h, d, dc, Ec, As, Asc, Es, fy, fyc, fck,l,Ef, Af1, ff, ea, et, nome):
    camadas = 6
    df = h + 3.5 * ea + 3 * et


    # Deformações normativas
    eps_ca = 0.0035
    eps_si = 0.010

    # ===============================
    # LIMITES DE DOMÍNIO
    # ===============================

    x23 = 0.259 * d
    eps_yd = (fy / 1.15) / Es
    xlim = (0.0035 / (0.0035 + eps_yd)) * d

    # ===============================
    # ESTIMATIVA INICIAL (tensões máximas)
    # ===============================
    Af =  Af1 * bw * camadas
    x = (fy * As + ff * Af - fyc * Asc) / (0.8 * bw * fck)

    # ===============================
    # DETERMINAÇÃO DA POSIÇÃO DA LINHA NEUTRA
    # ===============================
    tol = 1e-4
    max_iter = 100
    for i in range(max_iter):
        x_old = x

        # ---- Verificação do domínio ----
        if x  < x23:
            dominio = 2
            eps_s = eps_si
            eps_c = (x / (d - x)) * eps_s


        else:  # Se for maior que x23, usa a geometria do Domínio 3 e 4
            dominio = 3
            eps_c = eps_ca
            eps_s = ((d - x) / x) * eps_c


        eps_sc = ((x - dc) / (d - x)) * eps_s
        eps_f = ((df - x) / (d - x)) * eps_s

        # ---- Tensões  ----
        sigma_s = min(Es * eps_s, fy)
        sigma_sc = min(Es * eps_sc, fyc)
        sigma_f = min(Ef * eps_f, ff)
        sigma_c = fck

        # ---- Novo x pelo equilíbrio ----
        x_calc = (sigma_s * As + sigma_f * Af - sigma_sc * Asc) / (0.8 * bw * sigma_c)

        # ---- Critério de convergência ----
        if abs(x_calc - x_old) <= tol:
            x = x_calc
            break
        x = 0.5 * (x_old + x_calc)
    else:
        print("Não convergiu")

     # ===============================
    # VERIFICAÇÃO FINAL DE DOMÍNIO 4
    # ===============================
    if x > xlim:
        print("\n❌ Seção em Domínio 4.")
        print(f"Linha neutra final ({x:.2f} cm) ultrapassou o limite ({xlim:.2f} cm).")
        print("O reforço têxtil não é admissível para esta configuração.")
        return None, None, None, None, camadas, nome


    # ===============================
    # DETERMINAÇÃO DO MOMENTO ÚLTIMO
    # ===============================

    Mu = ((sigma_s*0.1) * As * d + (sigma_f*0.1)  * Af * df - 0.32 * bw * (sigma_c*0.1)  * x ** 2 - (sigma_sc*0.1)  * Asc * dc )  # Conversão: MPa → kN/cm² (1 MPa = 0.1 kN/cm²)
    P = (Mu * 6) / l
    return dominio, x, Mu, P, camadas, nome


def main():
    bw, h, d, dc, Ec, As, Asc, Es, fy, fyc, fck,l = dados_de_entrada()
    Ef, Af1, ff, ea, et, nome = escolher_textil()
    dominio,x,Mu,P,camadas,nome = dimensionar_reforco(bw, h, d, dc, Ec, As, Asc, Es, fy, fyc, fck,l,Ef, Af1, ff,ea,et,nome)



    # ===============================
    # RESULTADOS
    # ===============================
    print("=" * 50)
    print("RESULTADOS")
    print("=" * 50)
    print(f"A viga se encontra no domínio = {dominio}")
    print(f"Posição da linha neutra (x) = {x:.3f} cm")
    print(f"Momento Resistente (Mr) = {Mu:.3f} Kn.cm")
    print(f" P = {P:.2f} kN")
    print(f" O reforço necessário é de {camadas} camadas do concreto têxtil {nome}.")
    print("Programa finalizado!")

if __name__ == "__main__":
    main()