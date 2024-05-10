# Hashzap
# botao de iniciar chat
# popup para entrar no chat
# quando entrar no chat: (aparece para todo mundo)
    # a mensagem que você entrou no chat
    # o campo e o botão de enviar mensagem
# a cada mensagem que você envia (aparece para todo mundo)
    # Nome: Texto da Mensagem



import flet as ft

def main(pagina):
    texto = ft.Text("Zap Gui")
    chat = ft.Column()
    nome_usuario = ft.TextField(label="Escreva seu nome")
    
    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem.get("tipo")
        if tipo == "mensagem":
            texto_mensagem = mensagem.get("texto")
            usuario_mensagem = mensagem.get("usuario")
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}"))
        elif tipo == "arquivo":
            usuario_mensagem = mensagem.get("usuario")
            nome_arquivo = mensagem.get("nome_arquivo")
            tipo_arquivo = mensagem.get("tipo_arquivo")
            if tipo_arquivo == "foto":
                chat.controls.append(ft.Text(f"{usuario_mensagem} enviou uma foto: {nome_arquivo}"))
            elif tipo_arquivo == "video":
                chat.controls.append(ft.Text(f"{usuario_mensagem} enviou um vídeo: {nome_arquivo}"))
            else:
                chat.controls.append(ft.Text(f"{usuario_mensagem} enviou um arquivo: {nome_arquivo}"))
        else:
            usuario_mensagem = mensagem.get("usuario")
            chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat", 
                                          size=12, italic=True, color=ft.colors.ORANGE_500))
        pagina.update()

    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    def enviar_mensagem(evento):
        mensagem = {"texto": campo_mensagem.value, "usuario": nome_usuario.value, "tipo": "mensagem"}
        enviar_mensagem_para_tunel(mensagem)
        limpar_campo_mensagem()

    def enviar_arquivo(tipo_arquivo):
        nome_arquivo = "arquivo.txt"  # Substitua isso com a lógica para obter o nome do arquivo real
        mensagem = {"usuario": nome_usuario.value, "nome_arquivo": nome_arquivo, "tipo_arquivo": tipo_arquivo, "tipo": "arquivo"}
        enviar_mensagem_para_tunel(mensagem)

    def enviar_mensagem_para_tunel(mensagem):
        pagina.pubsub.send_all(mensagem)
        pagina.update()

    def limpar_campo_mensagem():
        campo_mensagem.value = ""
        pagina.update()

    campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=enviar_mensagem)
    botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)
    botao_enviar_foto = ft.ElevatedButton("Enviar Foto", on_click=lambda _: enviar_arquivo("foto"))
    botao_enviar_video = ft.ElevatedButton("Enviar Vídeo", on_click=lambda _: enviar_arquivo("video"))

    def entrar_popup(evento):
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})
        pagina.add(chat)
        popup.open = False
        pagina.remove(botao_iniciar)
        pagina.remove(texto)
        pagina.add(ft.Row([campo_mensagem, botao_enviar_mensagem, botao_enviar_foto, botao_enviar_video]))
        pagina.update()

    popup = ft.AlertDialog(
        open=False, 
        modal=True,
        title=ft.Text("Bem vindo ao Zap Gui"),
        content=nome_usuario,
        actions=[ft.ElevatedButton("Entrar", on_click=entrar_popup)],
    )

    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat)

    pagina.add(texto)
    pagina.add(botao_iniciar)

ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
