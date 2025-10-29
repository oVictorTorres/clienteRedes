# Projeto 1 - Chat (Cliente)

Este é o componente **Cliente** (Desktop) do sistema de chat desenvolvido para a disciplina de Redes de Computadores.

Esta é a aplicação com interface gráfica (GUI) que o usuário utiliza para se conectar ao servidor, ver seus contatos e trocar mensagens.

## 🚀 Funcionalidades (Lado do Cliente)

* **Interface Gráfica:** Construído com `Tkinter` para fornecer uma janela de login e uma janela de chat.
* **Autenticação e Registro:** Permite que o usuário se registre ou faça login no servidor.
* **Lista de Contatos:** Exibe todos os usuários cadastrados e indica seu status (online/offline).
* **Chat em Tempo Real:** Permite o envio e recebimento de mensagens instantâneas.
* **Recebimento de Mensagens Offline:** Recebe e exibe todas as mensagens que foram enviadas enquanto o usuário estava offline, assim que faz o login.
* **Indicador "Digitando":** Mostra um aviso quando o outro usuário está digitando.
* **Persistência de Histórico:** Salva o histórico das conversas localmente e os carrega ao abrir uma conversa.
* **Concorrência (Threads):** Utiliza uma thread separada (`receive_messages`) para escutar o servidor, garantindo que a interface gráfica (GUI) não trave.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Bibliotecas Principais:**
    * `tkinter` (para a Interface Gráfica)
    * `socket` (para comunicação de rede TCP)
    * `threading` (para não travar a GUI)

## ⚡ Como Executar o Cliente

**Pré-requisitos:**
* Python 3 instalado.
* **O Servidor (`servidorRedes`) deve estar em execução.**

**Passos:**

1.  Clone este repositório:
    ```bash
    git clone [URL-DO-SEU-REPOSITORIO-CLIENTE]
    cd clienteRedes-main
    ```

2.  Execute o script do cliente:
    ```bash
    python cliente.py
    ```

3.  A janela de Login/Registro aparecerá.

4.  **Para testar o chat:** Você pode executar o `python cliente.py` em dois ou mais terminais diferentes para simular múltiplos usuários.

## 👤 Autor

* Victor Torres.
