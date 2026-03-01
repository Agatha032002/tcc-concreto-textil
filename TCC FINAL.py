import math

def cabecalho():
    print("=" * 70)
    print("CÁLCULO DE REFORÇO COM CONCRETO TÊXTIL - VIGA SUBMETIDA À FLEXÃO")
    print("UNIVERSIDADE FEDERAL DE SERGIPE")
    print("Aluna: Agatha Ferreira Oliveira")
    print("Orientador: Profº Dr. Emerson Figueiredo dos Santos")
    print("=" * 70)

# =====================================================
# =============== ENTRADA DE DADOS ====================
# =====================================================
def ler_dados(mensagem):
    while True:
        try:
            entrada = input(mensagem).replace(",", ".").strip()
            valor = float(entrada)
            return valor
        except ValueError:
            print("⚠️ Entrada inválida! Digite apenas números.")

def entrada_dados():
    while True:
        print("\n===== DADOS DE ENTRADA =====")
        bw = ler_dados('Digite a largura da viga (bw) em cm: ')
        h =  ler_dados('Digite a altura da viga (h) em cm: ')
        d =  ler_dados('Digite a distância do centro geométrico da armadura tracionada até a borda mais comprimida (d) em cm: ')
        dc = ler_dados( 'Digite a distância do centro geométrico da armadura comprimida até a borda mais comprimida (d) em cm: ')
        As = ler_dados('Digite a área de aço da armadura tracionada (As) em cm²: ')
        Asc = ler_dados('Digite a área de aço da armadura comprimida (Asc) em cm²: ')
        Ms = ler_dados('Digite o momento fletor que a viga deve resistir (Ms) em kN·cm: ')

        # Propriedades mecânicas (em MPa)
        Ec =  ler_dados('Digite o módulo de elasticidade do concreto (Ec) em GPa: ')
        Es =  ler_dados('Digite o módulo de elasticidade do aço (Es) em GPa: ')
        fy =  ler_dados('Digite a tensão de escoamento na armadura tracionada (em MPa): ')
        fyc = ler_dados('Digite a tensão de escoamento na armadura comprimida (em MPa): ')
        fck = ler_dados('Digite a resistência característica do concreto (fck) (em MPa): ')

        # -------- MOSTRAR RESUMO --------
        print("\n" + "=" * 50)
        print("RESUMO DOS DADOS INSERIDOS")
        print("=" * 50)
        print(f"bw  = {bw} cm")
        print(f"h   = {h} cm")
        print(f"d   = {d} cm")
        print(f"dc  = {dc} cm")
        print(f"As  = {As} cm²")
        print(f"Asc = {Asc} cm²")
        print(f"Ms  = {Ms} kN.cm")
        print(f"Ec  = {Ec} GPa")
        print(f"Es  = {Es} GPa")
        print(f"fy  = {fy} MPa")
        print(f"fyc = {fyc} MPa")
        print(f"fck = {fck} MPa")
        print("=" * 50)

        confirma = input("\nOs dados estão corretos? (s/n): ").lower().strip()

        if confirma.startswith('s'):
            return bw, h, d, dc, As, Asc, Ms, Ec, Es, fy, fyc, fck
        else:
            print("\n🔄 Refaça a entrada dos dados...\n")


# =====================================================
# ================= MÉTODO TRINTIN ====================
# =====================================================
def escolher_textil_trintin():

    # --- ESCOLHA DO TÊXTIL --- #

    while True:
        print("=" * 50)
        print("DADOS DO REFORÇO TÊXTIL PARA O MÉTODO TRINTIN")
        print("=" * 50)

        print('[1] Armo-mesh L500 da S&P')
        print('[2] AF - 0200 BR da FiberTEX')
        print('[3] Outro')

        op = int(input('Escolha a opção de têxtil para o reforço: '))

        if op == 1:
            print("Você escolheu a Armo-mesh L500 da S&P")
            return 240, 0.0105, 800, 0.3, 0.0105, "Armo-mesh L500 da S&P"  # Ef(GPa), Af1/cm(cm2/cm) ,σf(MPa), ea(cm),et(cm)


        elif op == 2:
            print("Você escolheu a AF - 0200 BR da FiberTEX")
            return 70, 0.0033, 220, 0.2, 0.05, "AF - 0200 BR da FiberTEX"  # Ef(GPa), Af1/cm(cm2/cm) ,σf(MPa), ea(cm),et(cm)


        elif op == 3:
            nome = input("Digite o nome do têxtil: ")
            Ef = float(input('Digite o módulo de elasticidade do têxti em GPa:'))
            g = float(input('Digite a gramatura da fibra na direção principal em g/m2'))
            p = float(input('Digite a densidade da fibra em g/cm3'))
            Af1 = ((g / 10000) / p)  # Af1/cm em (cm2/cm)
            ff = float(input(' Digite a tensão de escoamento do têxtil em MPa:'))
            ea = float(input('Digite a espessura da argamassa em cm:'))
            et = float(input(' Digite a espessura do têxtil em MPa:'))
            return Ef, Af1, ff, ea, et, nome

        else:
            print("Opção inválida!")
            continue

def metodo_trintin(dados):
    bw, h, d, dc, As, Asc, Ms, Ec, Es, fy, fyc, fck = dados
    Ef, Af1,ff,ea,et,nome = escolher_textil_trintin()

    camadas = 1
    while True:

        # ---Cálculo da Linha Neutra---#
        if camadas < 3:
            df = h

        elif 3 <= camadas < 6:
            df = h + 2 * ea + 1.5 * et

        elif camadas == 6:
            df = h + 3.5 * ea + 3 * et

        else:
            raise ValueError("\n⚠️ Dimensionamento inviável: mais de 6 camadas. Redimensione a seção.")

        Af = Af1 * camadas * bw

        a = 0.5 * Ec * bw
        b = (Es * (As + Asc)) + (Af * Ef)
        c = - ((Es * As * d) + (Asc * dc * Es) + (Af * Ef * df))

        x = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)

        Ix = (bw*x**3)/3 +(Es/Ec)*As*(d-x)**2 + (Es/Ec)*Asc*(x-dc)**2 + (Ef/Ec)*Af*(df-x)**2

        Mr = (Ec/Ef)*(((ff/10)*Ix)/(df-x))

        if Mr >= Ms:
            return x, Ix,Mr, camadas, nome

        camadas += 1


# =====================================================
# ================= MÉTODO BEEBER =====================
# =====================================================
def escolher_textil_beber():

    # --- ESCOLHA DO TÊXTIL --- #

    while True:
        print("=" * 50)
        print("DADOS DO REFORÇO TÊXTIL PARA O MÉTODO BEBER")
        print("=" * 50)

        print('[1] Armo-mesh L500 da S&P')
        print('[2] AF - 0200 BR da FiberTEX')
        print('[3] Outro')

        op = int(input('Escolha a opção de têxtil para o reforço: '))

        if op == 1:
            print("Você escolheu a Armo-mesh L500 da S&P")
            return  240000, 0.0105, 4300,0.3,0.0105,"Armo-mesh L500 da S&P"  # Ef(MPa),Af1p/cm (cm2/cm), σf (MPa), ea(cm),et (cm)

        elif op == 2:
            print("Você escolheu a AF - 0200 BR da FiberTEX")
            return 70000, 0.003269, 1000, 0.2,0.05,"AF - 0200 BR da FiberTEX" # Ef(MPa),Af1p/cm (cm2/cm), σf (MPa), ea(cm),et (cm)


        elif op == 3:
            nome = input("Digite o nome do têxtil: ")
            Ef = float(input('Digite o módulo de elasticidade do têxti em MPa:'))
            g = float(input('Digite a gramatura da fibra na direção principal em g/m2'))
            p = float(input('Digite a densidade da fibra em g/cm3'))
            Af1 = ((g / 10000) / p)  # Af1/cm em (cm2/cm)
            ff = float(input(' Digite a tensão de escoamento do têxtil em MPa:'))
            ea = float(input('Digite a espessura da argamassa em cm:'))
            et = float(input(' Digite a espessura do têxtil em MPa:'))
            return Ef, Af1, ff, ea, et, nome

        else:
            print("Opção inválida!")
            continue


def metodo_beeber(dados):

    bw, h, d, dc, As, Asc, Ms, Ec, Es, fy, fyc, fck = dados
    Ef, Af1, ff, ea, et, nome = escolher_textil_beber()

    # Conversão GPa → MPa
    Ecb = Ec * 1000
    Esb = Es * 1000
    Efb = Ef * 1000

    camadas = 1

    while True:
        # ---Cálculo de df  --- #
        if camadas < 3:
            df = h

        elif 3 <= camadas < 6:
            df = h + 2 * ea + 1.5 * et

        elif camadas == 6:
            df = h + 3.5 * ea + 3 * et

        else:
            raise ValueError("\n⚠️Dimensionamento inviável: mais de 6 camadas. Redimensione a seção.")

        # Deformações normativas
        eps_ca = 0.0035
        eps_si = 0.010

        # ===============================
        # LIMITES DE DOMÍNIO
        # ===============================

        x23 = 0.259 * d
        eps_yd = (fy / 1.15) / Esb
        xlim = (0.0035 / (0.0035 + eps_yd)) * d

        # ===============================
        # ESTIMATIVA INICIAL (tensões máximas)
        # ===============================
        Af = Af1 * bw * camadas
        x = (fy * As + ff * Af - fyc * Asc) / (0.8 * bw * 0.85 * (fck / 1.4))

        # ===============================
        # DETERMINAÇÃO DA POSIÇÃO DA LINHA NEUTRA
        # ===============================
        tol = 1e-4
        max_iter = 100
        for i in range(max_iter):
            x_old = x

            # ---- Verificação do domínio ----
            if x < x23:
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
            sigma_s = min(Esb * eps_s, fy)
            sigma_sc = max(min(Esb * eps_sc, fyc), -fy)
            sigma_f = min(Efb * eps_f, ff)
            sigma_c = 0.85 * (fck / 1.4)

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
            raise ValueError("O reforço têxtil não é admissível para esta configuração.")

        # ===============================
        # DETERMINAÇÃO DO MOMENTO ÚLTIMO
        # ===============================

        Mu = ((sigma_s * 0.1) * As * d + (sigma_f * 0.1) * Af * df - 0.32 * bw * (sigma_c * 0.1) * x ** 2 - (
                    sigma_sc * 0.1) * Asc * dc)
        # Conversão: MPa → kN/cm² (1 MPa = 0.1 kN/cm²)
        if Mu >= Ms:
            return x,dominio, Ms, Mu, camadas, nome
        else:
            camadas += 1




# =====================================================
# ===================== MENU ==========================
# =====================================================
def encerramento():
    while True:
        print("\n" + "=" * 40)
        print("[1] Voltar ao menu principal")
        print("[0] Sair do programa")
        print("=" * 40)

        op = input("Escolha: ").strip().lower()

        if op == "1":
            return

        elif op == "0":
            print("\nEncerrando o programa...")
            print("Obrigada!")
            exit()

        else:
            print("Opção inválida!")

def menu():

    cabecalho()

    dados = entrada_dados()

    while True:

        print("\n" + "=" * 50)
        print("MENU PRINCIPAL")
        print("=" * 50)
        print("[1] Calcular pelo Método de TRINTIN")
        print("[2] Calcular pelo Método de BEEBER")
        print("[3] Calcular pelos DOIS e comparar")
        print("[0] Sair")
        print("=" * 50)

        op = input("Escolha uma opção: ")

        # ================= TRINTIN =================
        if op == "1":

            try:
                X, Ix, Mr, camadas, nome = metodo_trintin(dados)

            except ValueError as e:
                print(f"\n⚠ {e}")
                continue  # volta pro menu sem quebrar o programa

            print("\n===== RESULTADO - TRINTIN =====")
            print(f"Posição da linha neutra (x) = {X:.3f} cm")
            print(f"Momento de Inercia (Ix) = {Ix:.3f} cm^4")
            print(f"Momento Resistente (Mr) = {Mr:.3f} kN.cm")
            print(f" O reforço necessário é de {camadas} camadas do concreto têxtil {nome}.")
            encerramento()


        # ================= BEEBER =================
        elif op == "2":

            try:
                x,dominio, Ms, Mu, camadas, nome = metodo_beeber(dados)

            except ValueError as e:
                print(f"\n⚠ {e}")
                continue  # volta pro menu sem quebrar o programa

            print("\n===== RESULTADO - BEEBER =====")
            print(f"A viga se encontra no domínio = {dominio}")
            print(f"Posição da linha neutra (x) = {x:.3f} cm")
            print(f"Momento Solicitante (Ms) = {Ms:.3f} kN.cm")
            print(f"Momento Resistente (Mr) = {Mu:.3f} kN.cm")
            print(f" O reforço necessário é de {camadas} camadas do concreto têxtil {nome}.")
            encerramento()

        # ================= COMPARAÇÃO =================
        elif op == "3":

            print("\n--- MÉTODO TRINTIN ---")
            try:
                x1, Ix,Mr, cam1, nome1 = metodo_trintin(dados)
            except ValueError as e:
                print(f"\n⚠ {e}")
                continue  # volta pro menu sem quebrar o programa

            print("\n--- MÉTODO BEEBER ---")
            try:
                x2, dominio2, Ms2, Mu2, cam2, nome2 = metodo_beeber(dados)
            except ValueError as e:
                print(f"\n⚠ {e}")
                continue  # volta pro menu sem quebrar o programa

            print("\n" + "=" * 100)
            print(f"{'TABELA COMPARATIVA':^100}")
            print("=" * 100)
            print(f"{'Método':^15}{'Têxtil':^25}{'x (cm)':^10}{'Momento (kN.cm)':^20}{'Camadas':^10}")
            print("-" * 100)
            print(f"{'Trintin':^15}{nome1:^25}{x1:^10.2f}{Mr:^20.2f}{cam1:^10}")
            print(f"{'Beeber':^15}{nome2:^25}{x2:^10.2f}{Mu2:^20.2f}{cam2:^10}")
            print("=" * 100)
            encerramento()


        elif op == "0":
            print("\nEncerrando programa...\n Obrigada!")
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu()