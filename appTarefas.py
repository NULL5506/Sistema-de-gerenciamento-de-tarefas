import PySimpleGUI as sg
import json

sg.theme('DefaultNoMoreNagging')
def salvar_tarefas(tarefas):
    with open("tarefas.json", "w") as file:
        json.dump(tarefas, file)
def carregar_tarefas():
    try:
        with open("tarefas.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
def criar_interface(tarefas):
    tarefas_ordenadas = sorted(tarefas, key=lambda x: (not x["Prioritária"], x["Título"]))

    layout = [
        [sg.Text("Lista de Tarefas", font=("Helvetica", 18))],
        [sg.Listbox(values=[f"{tarefa['Título']} - {tarefa['Descrição']} - {tarefa['Data de Vencimento']}" for tarefa in tarefas_ordenadas if not tarefa["Prioritária"]], size=(80, 10), key="-LIST-")],
        [sg.Text("_" * 80)],
        [sg.Text("Tarefas Priorizadas", font=("Helvetica", 14))],
        [sg.Listbox(values=[f"{tarefa['Título']} - {tarefa['Descrição']} - {tarefa['Data de Vencimento']}" for tarefa in tarefas_ordenadas if tarefa["Prioritária"]], size=(80, 5), key="-LIST-PRIORITARIAS-")],
        [sg.Button("Criar Tarefa"), sg.Button("Atualizar Tarefa"), sg.Button("Remover Tarefa"), sg.Button("Priorizar Tarefa"), sg.Button("Sair")]
    ]

    return sg.Window("Gerenciador de Tarefas", layout, finalize=True)

def criar_nova_tarefa():
    layout = [
        [sg.Text("Criar Nova Tarefa", font=("Helvetica", 18))],
        [sg.Text("Título"), sg.InputText(key="-TITULO-")],
        [sg.Text("Descrição"), sg.InputText(key="-DESCRICAO-")],
        [sg.Text("Data de Vencimento"), sg.InputText(key="-DATA-")],
        [sg.Button("Criar"), sg.Button("Cancelar")]
    ]
    window = sg.Window("Criar Nova Tarefa", layout, finalize=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cancelar"):
            break
        elif event == "Criar":
            novo_titulo = values["-TITULO-"]
            nova_tarefa = {
                "Título": novo_titulo,
                "Descrição": values["-DESCRICAO-"],
                "Data de Vencimento": values["-DATA-"],
                "Concluída": False,
                "Prioritária": False
            }
            tarefas.append(nova_tarefa)
            salvar_tarefas(tarefas)
            sg.popup(f"Tarefa '{novo_titulo}' criada com sucesso!")
            break

    window.close()
def atualizar_tarefa(tarefas):
    layout = [
        [sg.Text("Atualizar Tarefa", font=("Helvetica", 18))],
        [sg.Listbox(values=[tarefa["Título"] for tarefa in tarefas], size=(40, 10), key="-LIST-TITULOS-")],
        [sg.Text("Selecione a tarefa que deseja atualizar:")],
        [sg.InputCombo(values=[tarefa["Título"] for tarefa in tarefas], key="-TAREFA-")],
        [sg.Text("Novo Título:"), sg.InputText(key="-NOVO-TITULO-")],
        [sg.Text("Nova Descrição:"), sg.InputText(key="-NOVA-DESCRICAO-")],
        [sg.Text("Nova Data de Vencimento:"), sg.InputText(key="-NOVA-DATA-")],
        [sg.Button("Selecionar"), sg.Button("Cancelar")]
    ]
    window = sg.Window("Atualizar Tarefa", layout, finalize=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cancelar"):
            window.close()
            return None
        elif event == "Selecionar":
            tarefa_selecionada = values["-TAREFA-"]
            novo_titulo = values["-NOVO-TITULO-"]
            nova_descricao = values["-NOVA-DESCRICAO-"]
            nova_data = values["-NOVA-DATA-"]

            for tarefa in tarefas:
                if tarefa["Título"] == tarefa_selecionada:
                    tarefa["Título"] = novo_titulo if novo_titulo else tarefa["Título"]
                    tarefa["Descrição"] = nova_descricao if nova_descricao else tarefa["Descrição"]
                    tarefa["Data de Vencimento"] = nova_data if nova_data else tarefa["Data de Vencimento"]
                    salvar_tarefas(tarefas)
                    sg.popup(f"Tarefa '{tarefa_selecionada}' atualizada com sucesso!")
                    window.close()
                    return tarefa_selecionada

    window.close()
def remover_tarefa(tarefas):
    layout = [
        [sg.Text("Remover Tarefa", font=("Helvetica", 18))],
        [sg.Listbox(values=[tarefa["Título"] for tarefa in tarefas], size=(40, 10), key="-LIST-")],
        [sg.Text("Selecione a tarefa que deseja remover:")],
        [sg.InputCombo(values=[tarefa["Título"] for tarefa in tarefas], key="-TAREFA-")],
        [sg.Button("Remover"), sg.Button("Cancelar")]
    ]

    window = sg.Window("Remover Tarefa", layout, finalize=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cancelar"):
            break
        elif event == "Remover":
            tarefa_selecionada = values["-TAREFA-"]
            for tarefa in tarefas:
                if tarefa["Título"] == tarefa_selecionada:
                    tarefas.remove(tarefa)
                    salvar_tarefas(tarefas)
                    sg.popup(f"Tarefa '{tarefa_selecionada}' removida com sucesso!")
                    break

    window.close()
def priorizar_tarefa(tarefas):
    layout = [
        [sg.Text("Priorizar Tarefa", font=("Helvetica", 18))],
        [sg.Listbox(values=[f"{tarefa['Título']} - {tarefa['Descrição']} - {tarefa['Data de Vencimento']}" for tarefa in tarefas], size=(40, 10), key="-LIST-")],
        [sg.Text("Selecione a tarefa que deseja priorizar:")],
        [sg.InputCombo(values=[tarefa["Título"] for tarefa in tarefas], key="-TAREFA-")],
        [sg.Button("Priorizar"), sg.Button("Cancelar")]
    ]
    popup_window = sg.Window("Priorizar Tarefa", layout, finalize=True)

    while True:
        event, values = popup_window.read()

        if event in (sg.WIN_CLOSED, "Cancelar"):
            popup_window.close()
            return None
        elif event == "Priorizar":
            tarefa_selecionada = values["-TAREFA-"]
            popup_window.close()
            return tarefa_selecionada
def main():
    global tarefas
    tarefas = carregar_tarefas()
    window = criar_interface(tarefas)

    while True:
        event, _ = window.read()

        if event in (sg.WIN_CLOSED, "Sair"):
            break
        elif event == "Criar Tarefa":
            criar_nova_tarefa()
            tarefas_ordenadas = sorted(tarefas, key=lambda x: (not x["Prioritária"], x["Título"]))
            window["-LIST-"].update(values=[f"{tarefa['Título']} - {tarefa['Descrição']} - {tarefa['Data de Vencimento']}" for tarefa in tarefas_ordenadas if not tarefa["Prioritária"]])
            window["-LIST-PRIORITARIAS-"].update(values=[f"{tarefa['Título']} - {tarefa['Descrição']} - {tarefa['Data de Vencimento']}" for tarefa in tarefas_ordenadas if tarefa["Prioritária"]])
        elif event == "Atualizar Tarefa":
            atualizar_tarefa(tarefas)
            tarefas_ordenadas = sorted(tarefas, key=lambda x: (not x["Prioritária"], x["Título"]))
            window["-LIST-"].update(values=[f"{tarefa['Título']} - {tarefa['Descrição']} - {tarefa['Data de Vencimento']}" for tarefa in tarefas_ordenadas if not tarefa["Prioritária"]])
            window["-LIST-PRIORITARIAS-"].update(values=[f"{tarefa['Título']} - {tarefa['Descrição']} - {tarefa['Data de Vencimento']}" for tarefa in tarefas_ordenadas if tarefa["Prioritária"]])
        elif event == "Remover Tarefa":
            remover_tarefa(tarefas)
            tarefas_ordenadas = sorted(tarefas, key=lambda x: (not x["Prioritária"], x["Título"]))
            window["-LIST-"].update(values=[f"{tarefa['Título']} - {tarefa['Descrição']} - {tarefa['Data de Vencimento']}" for tarefa in tarefas_ordenadas if not tarefa["Prioritária"]])
            window["-LIST-PRIORITARIAS-"].update(values=[f"{tarefa['Título']} - {tarefa['Descrição']} - {tarefa['Data de Vencimento']}" for tarefa in tarefas_ordenadas if tarefa["Prioritária"]])
        elif event == "Priorizar Tarefa":
            tarefa_prioritaria = priorizar_tarefa(tarefas)
            if tarefa_prioritaria is not None:
                for tarefa in tarefas:
                    if tarefa["Título"] == tarefa_prioritaria:
                        tarefa["Prioritária"] = True
                        salvar_tarefas(tarefas)
                        sg.popup(f"Tarefa '{tarefa_prioritaria}' prioritária marcada com sucesso!")
                        tarefas_ordenadas = sorted(tarefas, key=lambda x: (not tarefa["Prioritária"], tarefa["Título"]))
                        window["-LIST-"].update(values=[f"{tarefa['Título']} - {tarefa['Descrição']} - {tarefa['Data de Vencimento']}" for tarefa in tarefas_ordenadas if not tarefa["Prioritária"]])
                        window["-LIST-PRIORITARIAS-"].update(values=[f"{tarefa['Título']} - {tarefa['Descrição']} - {tarefa['Data de Vencimento']}" for tarefa in tarefas_ordenadas if tarefa["Prioritária"]])
                        break

    window.close()

if __name__ == "__main__":
    main()