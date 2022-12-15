from tkinter import *
from tkinter import filedialog
from pytube import YouTube
from pytube import Playlist
from time import sleep
import shutil


# Função de seleção de pasta
def selecione():
    pasta.delete(0, len(pasta.get()))
    pasta.insert(0, filedialog.askdirectory())


def seleciona_arquivo():
    arquivo_local.delete(0, len(arquivo_local.get()))
    arquivo_local.insert(0, filedialog.askopenfile().name)


# Função botão baixar
def baixar():
    if campo_link.get() != "":
        if campo_link.get().find("https://youtube.com/playlist", 1, 28):
            label_status.config(text=f"Baixando playlist")
            download_playlist(campo_link.get())
        else:
            download_link(campo_link.get())
    elif arquivo_local.get() != "":
        print("Arquivo")
        download_arquivo(arquivo_local.get())


# rotina que recebe cada link para download
def download_link(link):
    try:
        yt = YouTube(link)
        label_status.config(text=f"Baixando video: \n {yt.title}\n Aguarde o término do processo!")
        sleep(5)
        ys = yt.streams.get_highest_resolution()
        arquivo = ys.download()
        shutil.move(arquivo, pasta.get())
        label_status.config(text=f"Download do vídeo: \n{yt.title}\n concluído")
    except Exception as e:
        label_status.config(text=e)


# rotina de download direto de arquivo txt
def download_arquivo(endereco):
    with open(endereco) as arquivo:
        for link in arquivo:
            download_link(link)


# rotina de playlist
def download_playlist(playlist):
    pl = Playlist(playlist)
    print(f"Baixando Playlist: {pl.title}")
    for video in pl.videos:
        arquivo = video.streams.get_highest_resolution().download()
        shutil.move(arquivo, pasta.get())
        label_status.config(text=f"Download do vídeo: \n{arquivo.title}\n concluído")

# criação da tela
screen = Tk()
title = screen.title("Youtube - Download de vídeos")
canvas = Canvas(screen, width=500, height=500)
canvas.pack()

# adicionando logo
logo = PhotoImage(file="logo.png")
logo = logo.subsample(5, 5)
canvas.create_image(250, 80, image=logo)

# criação do campo e label do link
campo_link = Entry(screen, width=60)
link_label = Label(screen, text="Informe o Link para Download, \nou selecione um arquivo txt com os links no segundo campo", font={"Arial", 12})
canvas.create_window(250, 150, window=link_label)
canvas.create_window(250, 180, window=campo_link)

# criação do campo para informar onde salvar os vídeos
label_pasta = Label(screen, text="Informe onde salvar os vídeos", font={"Arial", 12})
pasta = Entry(screen, width=60)
select_btn = Button(screen, text="...", command=selecione)
canvas.create_window(250, 250, window=label_pasta)
canvas.create_window(250, 270, window=pasta)
pasta.insert(0, "C:/")
canvas.create_window(440, 270, window=select_btn)
label_status = Label(screen, text="", font={"Arial", 12})
canvas.create_window(250, 400, window=label_status)

arquivo_local = Entry(screen, width=60)
canvas.create_window(250, 210, window=arquivo_local)
arquivo_select = Button(screen, text="...", command=seleciona_arquivo)
canvas.create_window(440,210, window=arquivo_select)
# botão download
btn_download = Button(screen, text="Baixar", background="#00FF00", command=baixar)
canvas.create_window(250, 470, window=btn_download)

screen.mainloop()
