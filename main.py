import flet as ft

def main(page: ft.Page):
    page.title = "EcoDrop ♻️"
    user, lixo, pts = {}, [], [0]

    def limpar(c="#EAF5E9"):
        page.controls.clear(); page.bgcolor=c

    def msg(t):
        page.snack_bar=ft.SnackBar(ft.Text(t)); page.snack_bar.open=True; page.update()

    def btn(t,f):
        return ft.ElevatedButton(t,on_click=f,width=280)

    def campo(t,s=False,v=""):
        return ft.TextField(label=t,width=300,value=v,password=s,color="white",
                            label_style=ft.TextStyle(color="white"))

    def bloco(t,d,i,c,f):
        return ft.Container(ft.Column([
            ft.Text(i,size=28),ft.Text(t,size=17,weight="bold",color="#123D2A"),
            ft.Text(d,size=12,color="#527060"),ft.Text("Acessar →",size=11,color="#176B3A")
        ],spacing=3),bgcolor=c,padding=14,border_radius=18,width=145,on_click=f)

    def tela(x,esp=12):
        limpar("#0B5D3B"); page.add(ft.Column(x,horizontal_alignment="center",spacing=esp)); page.update()

    def login(e=None):
        em,sn=campo("E-mail"),campo("Senha",True)
        def entrar(e):
            inicio() if em.value==user.get("email") and sn.value==user.get("senha") else msg("E-mail ou senha incorretos.")
        tela([
            ft.Text("♻️ EcoDrop",size=38,weight="bold",color="white"),
            ft.Text("Descarte eletrônico consciente",color="#D9F5E5"),em,sn,
            btn("Entrar",entrar),
            ft.TextButton("Criar conta",on_click=cadastro,style=ft.ButtonStyle(color="white"))
        ])

    def cadastro(e=None):
        campos=[campo(x) for x in ["Nome","E-mail","Senha","Cidade"]]
        def salvar(e):
            if not all(x.value for x in campos): return msg("Preencha todos os campos.")
            user.update(dict(zip(["nome","email","senha","cidade"],[x.value for x in campos])))
            msg("Conta criada!"); login()
        tela([ft.Text("Criar conta",size=30,weight="bold",color="white"),*campos,
              btn("Cadastrar",salvar),ft.TextButton("Voltar",on_click=login)])

    def inicio(e=None):
        limpar()
        page.add(ft.Column([
            ft.Row([ft.Column([ft.Text("Olá,",color="#527060"),
            ft.Text(user.get("nome","Usuário"),size=24,weight="bold",color="#123D2A")],spacing=0),
            ft.IconButton(ft.Icons.PERSON,on_click=perfil)],alignment="spaceBetween"),
            ft.Container(ft.Column([
                ft.Text("Cuide do planeta.",size=24,weight="bold",color="white"),
                ft.Text("Cada descarte faz diferença 🌱",color="#D9F5E5"),
                ft.Row([ft.Text(f"♻️ {len(lixo)}\nDescartes",color="white"),
                ft.Text(f"⭐ {pts[0]}\nEcoPoints",color="white")],alignment="spaceAround")
            ]),bgcolor="#176B3A",padding=18,border_radius=22),
            ft.Text("O que você deseja fazer?",size=19,weight="bold",color="#123D2A"),
            ft.Row([bloco("Descartar","Cadastre seu eletrônico","♻️","#D4F0D5",descarte),
                    bloco("Coleta","Encontre um ponto","📍","#DCEBD0",mapa)],alignment="center"),
            ft.Row([bloco("EcoPoints","Veja recompensas","⭐","#E9E3B5",recompensas),
                    bloco("Perfil","Seus dados","👤","#D6E8D9",perfil)],alignment="center"),
            ft.Text("EcoDrop • reciclar é transformar 🌎",size=11,color="#527060")
        ],spacing=13)); page.update()

    def descarte(e=None):
        tipo=ft.Dropdown(label="Tipo",width=300,label_style=ft.TextStyle(color="white"),
            options=[ft.dropdown.Option(x) for x in ["Celular","Computador","Notebook","Tablet","TV","Bateria","Cabo","Outro"]])
        qtd=campo("Quantidade")
        def salvar(e):
            if not tipo.value or not qtd.value:return msg("Preencha os campos.")
            lixo.append((tipo.value,qtd.value));msg("Eletrônico cadastrado!");inicio()
        tela([ft.Text("Cadastrar eletrônico",size=27,weight="bold",color="white"),
               tipo,qtd,btn("Cadastrar",salvar),ft.TextButton("Voltar",on_click=inicio)])

    def mapa(e=None):
        cidade=campo("Sua cidade",v=user.get("cidade","")); lista=ft.Column()
        locais=[("EcoDrop Centro","Centro","Eletrônicos em geral"),
        ("EcoDrop Reciclagem","Bairro Central","Celulares e baterias"),
        ("Ponto Verde","Avenida Principal","Computadores e TVs")]
        def buscar(e):
            lista.controls.clear()
            for n,end,a in locais:
                lista.controls.append(ft.Container(ft.Row([
                    ft.Text("📍",size=25),ft.Column([ft.Text(n,weight="bold"),ft.Text(end),ft.Text(a,size=11)]),
                    ft.IconButton(ft.Icons.ARROW_FORWARD,on_click=lambda e,n=n,a=a:confirmar(n,a))
                ]),bgcolor="white",padding=10,border_radius=15))
            page.update()
        tela([ft.Text("Pontos de coleta",size=27,weight="bold",color="white"),
              cidade,btn("Buscar pontos",buscar),lista,ft.TextButton("Voltar",on_click=inicio)],10)

    def confirmar(nome,aceita):
        itens="\n".join(f"• {a} - {b}" for a,b in lixo) or "Nenhum item."
        def finalizar(e):
            pts[0]+=50;msg("+50 EcoPoints!");inicio()
        tela([ft.Text("Confirmar entrega",size=27,weight="bold",color="white"),
              ft.Text(f"📍 {nome}",size=20,color="white"),ft.Text(f"Aceita: {aceita}",color="#D9F5E5"),
              ft.Text(itens,color="white"),btn("Confirmar entrega",finalizar),
              ft.TextButton("Voltar",on_click=mapa)])

    def recompensas(e=None):
        def resgatar(v,n):
            if pts[0]>=v:pts[0]-=v;msg(n+" resgatada!");recompensas()
            else:msg("EcoPoints insuficientes.")
        tela([ft.Text("⭐ EcoPoints",size=28,weight="bold",color="white"),
              ft.Text(f"{pts[0]} pontos",size=24,color="white"),
              bloco("Recompensa Verde","50 pontos","🌱","#D4F0D5",lambda e:resgatar(50,"Recompensa")),
              bloco("Recompensa Sustentável","100 pontos","♻️","#DCEBD0",lambda e:resgatar(100,"Recompensa")),
              ft.TextButton("Voltar",on_click=inicio)])

    def perfil(e=None):
        tela([ft.Text("Meu perfil",size=28,weight="bold",color="white"),ft.Text("👤",size=50),
              ft.Text(user.get("nome",""),size=21,color="white"),
              ft.Text(f"📧 {user.get('email','')}",color="white"),
              ft.Text(f"📍 {user.get('cidade','')}",color="white"),ft.Divider(color="white"),
              ft.Text(f"♻️ Descartes: {len(lixo)}",color="white"),
              ft.Text(f"⭐ EcoPoints: {pts[0]}",color="white"),btn("Voltar",inicio),
              ft.TextButton("Sair",on_click=login)],10)

    login()

ft.app(target=main)