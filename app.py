"""
Semana de la Ciencia · Matemática
Ronda 1: "¡Puedo adivinar tu número!"  +  Código 11: "Descifrando el misterio matemático"

Ejecutar:  streamlit run app.py
"""
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Descifrando el misterio matemático", page_icon="🔢", layout="wide")


# ───────────────────────── Lógica matemática ─────────────────────────
def mult11_steps(n: int):
    """Algoritmo 'de las sumas adyacentes' para n × 11, con llevadas.

    Se rodea al número de ceros: 0 d1 d2 ... dk 0 y se suman cifras vecinas.
    Devuelve una tabla (de izquierda a derecha) y el resultado reconstruido.
    """
    digits = [int(c) for c in str(n)]
    padded = [0] + digits + [0]
    sums = [padded[i] + padded[i + 1] for i in range(len(padded) - 1)]

    carry_in, out_digits, carries_out = 0, [], []
    for s in reversed(sums):  # de derecha a izquierda
        total = s + carry_in
        out_digits.append(total % 10)
        carries_out.append(total // 10)
        carry_in = total // 10
    carries_in = [0] + carries_out[:-1]  # llevada que recibe cada posición
    final_carry = carries_out[-1]
    if final_carry:
        out_digits.append(final_carry)

    result = int("".join(str(d) for d in reversed(out_digits)))
    assert result == n * 11
    rows = {
        "Suma de vecinas": sums,
        "Llevada que recibe": list(reversed(carries_in)),
        "Cifra que se escribe": list(reversed(out_digits[: len(sums)])),
    }
    labels = [f"posición {i + 1}" for i in range(len(sums))]
    df = pd.DataFrame(rows, index=labels).T
    return df, result, any(c > 0 for c in carries_out)


def has_carry(n: int) -> bool:
    return mult11_steps(n)[2]


def parse_int(txt: str):
    try:
        return int(str(txt).strip())
    except ValueError:
        return None


# ───────────────────────── Contenido didáctico ─────────────────────────
LEVELS = {
    1: dict(
        titulo="Primer nivel: cuando parece magia",
        consigna="Calculen mentalmente y expliquen qué observan.",
        nums=[3, 5, 7, 9],
        reflexion="¿Qué observan en los resultados? ¿Cómo explicarían por qué pasa?",
        docente=dict(
            intencion="Instalar una primera regularidad (la cifra se repite) y habilitar la pregunta por el *porqué*. "
            "Es el momento de 'lo mágico': todavía no se pide demostrar, sí poner en palabras.",
            esperable="Responden 33, 55, 77, 99 y dicen 'se repite el número'. Algunos recurren a la tabla del 11.",
            errores="Quedarse en 'da lo mismo dos veces' sin explicar; creer que el truco es 'poner el número dos veces' (¿y 10×11?).",
            preguntas=["¿Pasa con 4×11? ¿Con 10×11?", "¿Cómo pensarías 3×11 si no supieras la tabla? (3×10 + 3)", "¿Hasta dónde creen que funciona?"],
            cierre="n × 11 = n × 10 + n. Aparece 11 = 10 + 1 como idea organizadora de todo lo que sigue.",
        ),
    ),
    2: dict(
        titulo="Segundo nivel: dos cifras y una primera regularidad",
        consigna="Sin utilizar la calculadora, anticipen los resultados.",
        nums=[12, 23, 31, 42, 53, 64],
        reflexion="¿Qué regla usaron para anticipar? Escríbanla con sus palabras.",
        docente=dict(
            intencion="Pasar de la repetición a la regla 'abro con la 1.ª cifra, en el medio la suma, cierro con la 2.ª'.",
            esperable="132, 253, 341, 462, 583. Formulan: 'las cifras se separan y en el medio va la suma'.",
            errores="Escribir 'las dos cifras originales con la suma al lado' (ej. 1 2 3). En el 64 aparece 6+4 = 10 y escriben 6104.",
            preguntas=["¿Qué cifra va en el medio y por qué?", "¿Qué pasó con el 64? ¿Alguien lo anticipó distinto?"],
            cierre="⚠️ Ojo docente: el 64 (6+4 = 10 → 704) ya trae una llevada, aunque el nivel se presenta como 'primera regularidad'. "
            "Puede ser un buen caso de tensión que anticipe el nivel 3, o reemplazarlo por 63 si querés un nivel 'limpio'.",
        ),
    ),
    3: dict(
        titulo="Tercer nivel: el misterio de las sumas que superan 9",
        intro="Ahora la regularidad parece complicarse.",
        consigna="Anticipen los resultados y expliquen qué cambia.",
        nums=[27, 38, 46, 78, 96],
        reflexion="¿Qué cambia respecto del nivel anterior? ¿Cómo se arregla la regla?",
        docente=dict(
            intencion="Generar conflicto cognitivo: la regla anterior produce 'cifras' de dos dígitos. Se resignifica con valor posicional (llevada).",
            esperable="297, 418, 506, 858, 1056. Dicen: 'si la suma pasa de 9, se lleva 1 a la cifra de la izquierda'.",
            errores="Escribir 3 11 8 → 3118; olvidar sumar la llevada; sorprenderse con 96×11 = 1056 (el resultado gana una cifra).",
            preguntas=["¿Por qué la llevada es 1 y nunca 2? (suma máxima de dos cifras: 18)", "¿Qué diferencia hay entre 27 y 38?"],
            cierre="⚠️ Caso límite: 27 → 2+7 = 9 'no supera 9' y no hay llevada (297). Sirve para precisar la condición. "
            "Además 96 → 1056 muestra que el producto puede ganar una cifra.",
        ),
    ),
    4: dict(
        titulo="Cuarto nivel: ¿el truco funciona con números de tres cifras?",
        consigna="Antes de calcular, escriban una conjetura sobre lo que podría suceder.",
        nums=[123, 214, 321, 472, 506],
        reflexion="Ahora que calcularon: ¿se cumplió su conjetura? ¿Qué ajustarían?",
        docente=dict(
            intencion="Formular y poner a prueba una conjetura; generalizar la regla de 2 a 3 cifras.",
            esperable="Conjeturas del tipo 'va la 1.ª, luego dos sumas y la última'. 1353, 2354, 3531, 5192, 5566.",
            errores="Sumar las tres cifras juntas; olvidar una de las sumas intermedias; no ver la llevada en 472 (4, 11, 9, 2 → 5192).",
            preguntas=["¿Cuántas sumas intermedias hay? ¿Y con 4 cifras?", "¿Qué tiene de particular el 506? (el 0 del medio, sin llevadas)"],
            cierre="Para abc × 11: a, a+b, b+c, c (con llevadas). La conjetura se valida con casos y con 11 = 10 + 1.",
        ),
    ),
}

RONDA1_DOCENTE = dict(
    intencion="Introducir el 'truco de adivinar' como problema: ¿por qué siempre se puede? Prepara el pasaje de lo aritmético a lo algebraico.",
    esperable="Al probar con varios números notan que el resultado crece de 6 en 6 y que siempre termina en 18 al 'sacar' lo que depende del número.",
    errores="Operar sin respetar el orden; creer que el truco 'funciona solo con números chicos'.",
    preguntas=["¿Qué pasa si dos personas piensan el mismo número?", "¿Qué pasa si cambio el 12 por otro número? ¿Y el 3?", "¿Podemos inventar un truco nuevo?"],
    cierre="(3n + 12)·2 − 6 = 6n + 18 → n = (resultado − 18) / 6. La expresión algebraica explica y permite 'diseñar' trucos.",
)


# ───────────────────────── Componentes reutilizables ─────────────────────────
def teacher_notes(d: dict, docente: bool):
    if not docente:
        return
    with st.expander("🧑‍🏫 Notas para el docente", expanded=False):
        st.markdown(f"**Intención didáctica:** {d['intencion']}")
        st.markdown(f"**Qué se espera:** {d['esperable']}")
        st.markdown(f"**Errores / obstáculos frecuentes:** {d['errores']}")
        st.markdown("**Preguntas para orientar la discusión:**")
        for q in d["preguntas"]:
            st.markdown(f"- {q}")
        st.markdown(f"**Cierre / institucionalización:** {d['cierre']}")


def show_steps(n: int):
    df, res, carry = mult11_steps(n)
    st.markdown(f"**{n} × 11 = {res}** — {'con llevada' if carry else 'sin llevadas'}")
    st.caption("Se rodea al número con ceros y se suman cifras vecinas, de derecha a izquierda.")
    st.dataframe(df, use_container_width=True)


def render_level(i: int, docente: bool):
    L = LEVELS[i]
    st.subheader(f"{i}. {L['titulo']}")
    if L.get("intro"):
        st.info(L["intro"])
    st.markdown(f"**Consigna:** {L['consigna']}")

    if i == 4:
        conj = st.text_area("✍️ Mi conjetura (antes de calcular):", key="r_n4_conjetura", height=100)
        if len(conj.strip()) < 10:
            st.warning("Escribí tu conjetura para habilitar los cálculos.")
            teacher_notes(L["docente"], docente)
            return

    st.markdown("##### Mis anticipaciones")
    cols = st.columns(min(len(L["nums"]), 3))
    for k, n in enumerate(L["nums"]):
        cols[k % len(cols)].text_input(f"{n} × 11 =", key=f"p_{i}_{n}")

    if st.button("✅ Comprobar", key=f"chk_{i}"):
        st.session_state[f"checked_{i}"] = True

    if st.session_state.get(f"checked_{i}"):
        ok = 0
        for n in L["nums"]:
            val = parse_int(st.session_state.get(f"p_{i}_{n}", ""))
            if val == n * 11:
                ok += 1
                st.success(f"{n} × 11 = {val} ✔")
            elif val is None:
                st.warning(f"{n} × 11: todavía no anticipaste un resultado.")
            else:
                st.error(f"{n} × 11 ≠ {val}. Revisá tu regla y probá de nuevo.")
        st.progress(ok / len(L["nums"]), text=f"{ok} de {len(L['nums'])} correctas")

        if st.toggle("🔍 Ver cómo funciona el truco paso a paso", key=f"steps_{i}"):
            for n in L["nums"]:
                show_steps(n)

        st.text_area(f"💬 {L['reflexion']}", key=f"r_n{i}_reflexion", height=120)

    teacher_notes(L["docente"], docente)


# ───────────────────────── Páginas ─────────────────────────
def page_inicio():
    st.title("🔢 Descifrando el misterio matemático")
    st.markdown(
        """
Una secuencia de actividades para **Semana de la Ciencia** que parte de la *magia* (adivinar números,
multiplicar por 11 "sin calcular") y llega a la *matemática* que la explica.

**Recorrido**

| Etapa | Pregunta central | Práctica matemática |
|---|---|---|
| **Ronda 1** | ¿Cómo adivina un número secreto? | Explorar, validar, pasar a lo algebraico |
| **Nivel 1** | ¿Qué pasa al multiplicar por 11? | Observar regularidades |
| **Nivel 2** | ¿Puedo anticipar sin calcular? | Formular una regla |
| **Nivel 3** | ¿Qué cambia si la suma supera 9? | Conflicto → valor posicional |
| **Nivel 4** | ¿Funciona con tres cifras? | Conjeturar y generalizar |
| **Nivel 5** | ¿Puedo inventar ejemplos que cumplan condiciones? | Argumentar y crear |
        """
    )
    st.info("Usá las pestañas de arriba. En la barra lateral podés activar el **Modo docente** para ver notas didácticas.")


def page_ronda1(docente: bool):
    st.subheader("Primera ronda: ¡puedo adivinar tu número!")
    st.markdown("**El coordinador dice:** *«Pensá un número en secreto. No me lo digas. Hacé las siguientes operaciones, en orden, y al final contame solamente el resultado».*")
    st.markdown(
        """
**El coordinador indica:**
1. Pensá un número.
2. Multiplicalo por 3.
3. Sumale 12.
4. Multiplicá el resultado por 2.
5. Restale 6.
6. Decime el resultado final.
        """
    )

    t1, t2, t3 = st.tabs(["🎩 Soy el adivinador", "🔎 ¿Por qué funciona?", "🛠️ Inventá tu truco"])

    with t1:
        res = st.number_input("Resultado que te dicen:", min_value=0, step=1, value=0, key="p_r1_resultado")
        if st.button("Adivinar", key="btn_r1"):
            if res < 18 or (res - 18) % 6 != 0:
                st.error("Ese resultado no puede salir si se siguieron bien los pasos. ¡Pedile que revise sus cuentas!")
            else:
                st.success(f"Tu número secreto era **{(res - 18) // 6}** 🎉")
        st.caption("Probá primero con compañeros. Después, ¿podés explicar cómo lo hace la app?")

    with t2:
        st.markdown("##### Exploración numérica")
        n_vals = list(range(1, 9))
        df = pd.DataFrame(
            {
                "Número pensado (n)": n_vals,
                "×3": [3 * n for n in n_vals],
                "+12": [3 * n + 12 for n in n_vals],
                "×2": [(3 * n + 12) * 2 for n in n_vals],
                "−6 (resultado)": [(3 * n + 12) * 2 - 6 for n in n_vals],
            }
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.text_area("¿Qué patrón ven en la última columna? ¿Qué pasa cada vez que n aumenta en 1?", key="r_r1_patron", height=100)
        if st.toggle("Ver la explicación algebraica", key="alg_r1"):
            st.latex(r"n \;\to\; 3n \;\to\; 3n+12 \;\to\; 2(3n+12)=6n+24 \;\to\; 6n+24-6 = 6n+18")
            st.markdown("El resultado es **6n + 18**, entonces para adivinar: **n = (resultado − 18) ÷ 6**.")

    with t3:
        st.markdown("Diseñá una secuencia: *pensá n → ×a → +b → ×c → −d*")
        c1, c2, c3, c4 = st.columns(4)
        a = c1.number_input("× a", 1, 20, 3, key="p_r1_a")
        b = c2.number_input("+ b", 0, 50, 12, key="p_r1_b")
        c = c3.number_input("× c", 1, 20, 2, key="p_r1_c")
        d = c4.number_input("− d", 0, 200, 6, key="p_r1_d")
        k, m = a * c, b * c - d
        st.latex(rf"c\,(a\,n+b)-d = {c}({a}n+{b})-{d} = {k}n + {m}")
        st.markdown(f"Para adivinar: **n = (resultado − ({m})) ÷ {k}**")
        n_test = st.number_input("Probalo con un número:", 0, 1000, 7, key="p_r1_test")
        r = c * (a * n_test + b) - d
        st.write(f"Resultado: **{r}** → la app deduce n = **{(r - m) / k:g}**")
        st.text_area("¿Qué condiciones debe cumplir tu truco para que siempre se pueda adivinar?", key="r_r1_condiciones", height=80)

    teacher_notes(RONDA1_DOCENTE, docente)


def page_nivel5(docente: bool):
    st.subheader("5. Quinto nivel: el desafío de inventar ejemplos")
    st.markdown(
        "En este momento, los estudiantes dejan de ser simples usuarios del truco y pasan a **poner a prueba la regularidad**."
    )
    st.markdown(
        """**Consigna:** En parejas, inventen tres multiplicaciones por 11 que cumplan estas condiciones:
- **A)** Una cuyo resultado se pueda anticipar fácilmente.
- **B)** Una en la que la suma de dos cifras supere 9.
- **C)** Una de tres cifras en la que se produzca al menos una llevada."""
    )

    c1, c2, c3 = st.columns(3)
    a = c1.text_input("A) ___ × 11", key="p_5_a")
    b = c2.text_input("B) ___ × 11", key="p_5_b")
    c = c3.text_input("C) ___ × 11", key="p_5_c")

    if st.button("🧪 Poner a prueba mis ejemplos", key="chk_5"):
        st.session_state["checked_5"] = True

    if st.session_state.get("checked_5"):
        na, nb, nc = parse_int(a), parse_int(b), parse_int(c)

        def check(n, cond, ok_msg, bad_msg, label):
            if n is None or n <= 0:
                st.warning(f"{label}: ingresá un número entero positivo.")
                return
            if cond(n):
                st.success(f"{label}: {n} × 11 = {n * 11}. {ok_msg}")
            else:
                st.error(f"{label}: {n} × 11 = {n * 11}. {bad_msg}")
            if st.toggle(f"Ver paso a paso ({n})", key=f"steps5_{label}"):
                show_steps(n)

        check(na, lambda n: not has_carry(n), "Se anticipa sin llevadas ✔", "Tiene llevadas, es más difícil de anticipar. Probá con cifras que sumen poco.", "A")
        check(nb, lambda n: 10 <= n <= 99 and sum(map(int, str(n))) > 9, "Las dos cifras suman más de 9 ✔", "Necesitás un número de dos cifras cuya suma sea mayor que 9.", "B")
        check(nc, lambda n: 100 <= n <= 999 and has_carry(n), "Tres cifras con llevada ✔", "Necesitás tres cifras y al menos una suma de vecinas mayor que 9.", "C")

        st.text_area("💬 Justifiquen: ¿por qué cada ejemplo cumple la condición? ¿Hay una forma de asegurarlo sin calcular?", key="r_n5_justificacion", height=130)
        st.text_area("🚀 Desafío extra: ¿qué pasaría con números de cuatro cifras? Escriban su conjetura.", key="r_n5_extra", height=90)

    teacher_notes(
        dict(
            intencion="Inversión del rol: los estudiantes *producen* casos para una propiedad. Inventar y justificar es una práctica matemática de alto nivel.",
            esperable="A: 21, 40, 112… (ninguna suma de vecinas supera 9). B: 58, 79, 96… C: 487, 565, 899…",
            errores="Pensar que B funciona con cualquier número de dos cifras; en C elegir 3 cifras sin llevada (ej. 123).",
            preguntas=["¿Puede haber dos cifras que sumen más de 9 y no haya llevada? (no)", "¿Cómo se diseña un número para tener llevada sin calcular?", "¿Cuántos ejemplos de A hay con dos cifras?"],
            cierre="Condición de llevada: alguna suma de cifras vecinas ≥ 10. Cada pareja presenta un ejemplo y el resto debe anticipar el resultado.",
        ),
        docente,
    )


def page_lab():
    st.subheader("🧪 Laboratorio del 11")
    st.markdown("Probá cualquier número y mirá cómo se arma el resultado.")
    n = st.number_input("Número:", min_value=1, max_value=10**9, value=472, step=1, key="p_lab")
    show_steps(int(n))


def page_registro():
    st.subheader("📋 Registro de la actividad")
    lines = [f"Registro generado el {datetime.now():%d/%m/%Y %H:%M}", f"Participante/Pareja: {st.session_state.get('nombre', '—')}", ""]
    for k in sorted(st.session_state.keys()):
        if (k.startswith("p_") or k.startswith("r_")) and str(st.session_state[k]).strip() not in ("", "0"):
            lines.append(f"[{k}] {st.session_state[k]}")
    text = "\n".join(lines)
    st.text_area("Vista previa", text, height=300, disabled=True)
    st.download_button("⬇️ Descargar registro (.txt)", text, file_name="registro_codigo11.txt")


# ───────────────────────── Main ─────────────────────────
with st.sidebar:
    st.header("⚙️ Opciones")
    st.text_input("Nombre / pareja", key="nombre")
    docente = st.toggle("Modo docente", value=False, help="Muestra intenciones didácticas, errores frecuentes y preguntas orientadoras.")

tabs = st.tabs(["🏠 Inicio", "🎩 Ronda 1", "Nivel 1", "Nivel 2", "Nivel 3", "Nivel 4", "Nivel 5", "🧪 Laboratorio", "📋 Registro"])
with tabs[0]:
    page_inicio()
with tabs[1]:
    page_ronda1(docente)
for idx in range(1, 5):
    with tabs[idx + 1]:
        render_level(idx, docente)
with tabs[6]:
    page_nivel5(docente)
with tabs[7]:
    page_lab()
with tabs[8]:
    page_registro()
