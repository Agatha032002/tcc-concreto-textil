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
      #  Ms = float(input('Digite o momento fletor que a viga deve resistir (Ms) em kN·cm: '))
        Es = float(input('Digite o módulo de elasticidade do aço (Es) em MPa: '))
        fy = float(input('Digite a tensão máxima na armadura tracionada (em MPa): '))
        fyc = float(input('Digite a tensão máxima na armadura comprimida (em MPa): '))
        fc = float(input('Digite a tensão máxima no concreto (em MPa): '))
        l = float (input('Digite a largura entre os apoios da viga (em cm)'))

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
       # print(f"Ms  = {Ms} kN·cm")
        print(f"Es = {Es} MPa")
        print(f"l = {l} MPa")
        print(f"fy = {fy} MPa")
        print(f"fyc = {fyc} MPa")
        print(f"fc = {fc} MPa")


        # ---- VERIFICAÇÃO ----
        confirma = input("\nOs dados estão corretos? (s/n): ").lower().strip()

        if confirma.startswith('s'):
            return bw, h, d, dc, Ec, As, Asc, Es, fy, fyc, fc,l

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
            return  240, 0.0117, 430,0.3,0.0117,"Armo-mesh L500 da S&P"  # Ef, Af1p/cm , Ff, ea,et

        elif op == 2:
            print("Você escolheu a AF - 0200 BR da FiberTEX")
            return 70, 0.0033, 100, 0.2,0.05,"AF - 0200 BR da FiberTEX" # Ef, Af1, ff, ea,et

        elif op == 3:
            nome = input("Digite o nome do têxtil: ")
            Ef = float(input('Digite o módulo de elasticidade do têxti em MPa:'))
            Af1 = float(input('Digite a área do textil para uma camada em cm:'))
            ff = float(input(' Digite a tensão de escoamento do têxtil em MPa:'))
            ea = float(input('Digite a espessura da argamassa em cm:'))
            et = float(input(' Digite a espessura do têxtil em MPa:'))
            return  Ef, Af1, ff,ea,et,nome


        else:
            print("Opção inválida!")
            continue

# --- DIMENSIONAMENTO DO REFORÇO --- #


def dimensionar_reforço(bw, h, d, dc, Ec, As, Asc, Es, fy, fyc,fc,l,Ef, Af1, ff,ea,et,nome):
    camadas = 3
    df = h + 2 * ea + 1.5 * et  ## Confirmar com professor

    # Deformações normativas
    eps_ca = 0.0035
    eps_s2 = 0.010

    # ===============================
    # LIMITES DE DOMÍNIO
    # ===============================

    x23 = 0.259 * d
    xlim = 0.595 *d

    # ===============================
    # ESTIMATIVA INICIAL (tensões máximas)
    # ===============================
    Af =  Af1 * bw * camadas
    x = (fy * As + ff * Af - fyc * Asc) / (0.8 * bw * fc)

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
            eps_s = eps_s2
            eps_c = (x / (d - x)) * eps_s

        elif x <= xlim:
            dominio = 3
            eps_c = eps_ca
            eps_s = ((d - x) / x) * eps_c

        if x > xlim:
            dominio = 4

            print("\n⚠️ Seção atingiu o Domínio 4")

            print(f"x = {x:.2f} cm  >  xlim = {xlim:.2f} cm")

            print("Reforço não admissível segundo a NBR 6118.")

            return None

        eps_sc = ((x - dc) / (d - x)) * eps_s
        eps_f = ((df - x) / (d - x)) * eps_s

        # ---- Tensões (modelos constitutivos) ----
        sigma_s = min(Es * eps_s, fy)
        sigma_sc = min(Es * eps_sc, fyc)
        sigma_f = min(Ef * eps_f, ff)
        sigma_c = 0.85*fc

        # ---- Novo x pelo equilíbrio ----
        x_calc = (sigma_s * As + sigma_f * Af - sigma_sc * Asc) / (0.8 * bw * sigma_c)

        # ---- Relaxação (média aritmética) ----
        x = 0.5 * (x_old + x_calc)

        # ---- Critério de convergência ----
        if abs(x - x_old) <= tol:
            print(f"Convergiu em {i + 1} iterações")
            break
    else:
        print("Não convergiu")


    # ===============================
    # DETERMINAÇÃO DO MOMENTO ÚLTIMO
    # ===============================

    Mu = (sigma_s  * As * d + sigma_f  * Af * df - 0.32 * bw * sigma_c  * x ** 2 - sigma_sc  * Asc * dc )

    P = (Mu * 6)/l
    return x, dominio, eps_c, eps_s, sigma_s, sigma_f, Mu , P


def main():
    bw, h, d, dc, Ec, As, Asc, Es, fy, fyc, fc, l= dados_de_entrada()
    Ef, Af1, ff, ea, et,nome = escolher_têxtil()

    resultado = dimensionar_reforço(bw, h, d, dc, Ec, As, Asc, Es, l, fy, fyc, fc,Ef, Af1, ff,ea,et,nome)
    if resultado is None:
        print("\nCálculo finalizado sem resultados numéricos.")
    else:
        x, dominio, eps_c, eps_s, sigma_s, sigma_f, Mu, P = dimensionar_reforço(bw, h, d, dc, Ec, As, Asc, Es, fy, fyc, fc,l,Ef, Af1, ff,ea,et,nome)


    # ===============================
    # RESULTADOS
    # ===============================
    print("=" * 50)
    print("RESULTADOS")
    print("=" * 50)
    print(f"x = {x:.4f} m")
    print(f"Domínio = {dominio}")
    print(f"εc = {eps_c:.5f}")
    print(f"εs = {eps_s:.5f}")
    print(f"σs = {sigma_s/1e6:.1f} MPa")
    print(f"σf = {sigma_f/1e6:.1f} MPa")
    print(f"Momento resistente M = {Mu / 1000:.2f} kN·cm")
    print ( f" P = {P:.2f} kN")

if __name__ == "__main__":
    main()