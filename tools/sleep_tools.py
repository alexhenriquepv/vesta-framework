def get_sleep_report(patient_id, date):
    """
    Simula a extração de um relatório de sono para um dia e retorna a string.
    """
    return (
        f"--- Relatório de sono Gerado (diário) ---\n"
        f"Relatório de sono do paciente {patient_id} em {date}:\n"
        f"- Duração do sono: 7.5 horas\n"
        f"- Qualidade do sono: 8/10\n"
    )

def get_month_sleep_report(patient_id, month, year):
    """
    Simula a extração de um relatório de sono para um mês e retorna a string.
    """
    return (
        f"--- Relatório de sono Gerado (mensal) ---\n"
        f"Relatório mensal de sono do paciente {patient_id} em {month}/{year}:\n"
        f"- Média de sono: 7.2 horas/noite\n"
        f"- Média de qualidade: 7.8/10\n"
    )



