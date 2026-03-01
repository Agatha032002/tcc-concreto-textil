import math


def metodo_trintin_web(bw, h, d, dc, As, Asc, Ms,Ec, Es, fy, fyc, fck, Ef, Af1, ff, ea, et, nome):

    camadas = 1

    while True:
        # --------- Cálculo de df ----------
        if camadas < 3:
            df = h

        elif 3 <= camadas < 6:
            df = h + 2 * ea + 1.5 * et

        elif camadas == 6:
            df = h + 3.5 * ea + 3 * et

        else:
            raise ValueError("Dimensionamento inviável: mais de 6 camadas. Redimensione a seção.")

        Af = Af1 * camadas * bw

        a = 0.5 * Ec * bw
        b = (Es * (As + Asc)) + (Af * Ef)
        c = - ((Es * As * d) + (Asc * dc * Es) + (Af * Ef * df))

        delta = b * b - 4 * a * c

        if delta < 0:
            raise ValueError("Equação sem solução real. Verifique os dados.")

        x = (-b + math.sqrt(delta)) / (2 * a)

        Ix = ((bw * x ** 3) / 3 + (Es / Ec) * As * (d - x) ** 2 + (Es / Ec) * Asc * (x - dc) ** 2 + (Ef / Ec) * Af * (df - x) ** 2 )

        Mr = (Ec / Ef) * (((ff / 10) * Ix) / (df - x))

        if Mr >= Ms:
            return { "x": x, "Ix": Ix, "Mr": Mr, "camadas": camadas,"nome": nome }

        camadas += 1

def metodo_beeber_web(bw, h, d, dc, As, Asc, Ms, Ec, Es, fy, fyc, fck,Ef, Af1, ff, ea, et, nome):

    # Conversão GPa → MPa
    Ecb = Ec * 1000
    Esb = Es * 1000
    Efb = Ef * 1000

    camadas = 1

    while True:

        # --------- Cálculo de df ----------
        if camadas < 3:
            df = h

        elif 3 <= camadas < 6:
            df = h + 2 * ea + 1.5 * et

        elif camadas == 6:
            df = h + 3.5 * ea + 3 * et

        else:
            raise ValueError("Dimensionamento inviável: mais de 6 camadas. Redimensione a seção.")

        eps_ca = 0.0035
        eps_si = 0.010

        x23 = 0.259 * d
        eps_yd = (fy / 1.15) / Esb
        xlim = (0.0035 / (0.0035 + eps_yd)) * d

        Af = Af1 * bw * camadas

        # Estimativa inicial
        x = (fy * As + ff * Af - fyc * Asc) / (0.8 * bw * 0.85 * (fck / 1.4))

        tol = 1e-4
        max_iter = 100

        for _ in range(max_iter):

            x_old = x

            # Verificação de domínio
            if x < x23:
                dominio = 2
                eps_s = eps_si
                eps_c = (x / (d - x)) * eps_s
            else:
                dominio = 3
                eps_c = eps_ca
                eps_s = ((d - x) / x) * eps_c

            eps_sc = ((x - dc) / (d - x)) * eps_s
            eps_f = ((df - x) / (d - x)) * eps_s

            sigma_s = min(Esb * eps_s, fy)
            sigma_sc = max(min(Esb * eps_sc, fyc), -fy)
            sigma_f = min(Efb * eps_f, ff)
            sigma_c = 0.85 * (fck / 1.4)

            x_calc = ( (sigma_s * As + sigma_f * Af - sigma_sc * Asc)/ (0.8 * bw * sigma_c))

            if abs(x_calc - x_old) <= tol:
                x = x_calc
                break

            x = 0.5 * (x_old + x_calc)

        else:
            raise ValueError("Não convergiu.")

        # Verificação Domínio 4
        if x > xlim:
            raise ValueError("Seção em Domínio 4. Reforço têxtil não admissível.")

        # Momento último
        Mu = ((sigma_s * 0.1) * As * d+ (sigma_f * 0.1) * Af * df- 0.32 * bw * (sigma_c * 0.1) * x ** 2- (sigma_sc * 0.1) * Asc * dc)

        if Mu >= Ms:
            return {"x": x,"dominio": dominio,"Ms": Ms,"Mu": Mu,"camadas": camadas,"nome": nome}

        camadas += 1