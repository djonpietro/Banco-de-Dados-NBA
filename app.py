from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

def query_db(query):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='24120603',
        database='NBA'
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consulta', methods=['POST'])
def consulta():
    query_number = request.form.get('query')
    queries = {
        '1': """
            with Times_Lebron as (
                select distinct ID_Time
                from Equipe
                where ID_Time in (select ID_Time
                                  from Jogador j natural join Joga_Em
                                  where j.nome='Lebron James')
            )

            select Cidade, Equipe.Apelido
            from Equipe natural join Times_Lebron;
        """,
        '2': """
            with Contagem_Temporada as (
                select ID_Time,
                       ID_Jogador,
                       count(Temporada) as Num_Temporadas
                from Joga_Em
                group by ID_Time, ID_Jogador
            )

            select j.Nome,
                   e.Cidade,
                   e.Apelido,
                   ct.Num_Temporadas
            from Jogador j natural join Contagem_Temporada ct natural join Equipe e
            order by Num_Temporadas desc limit 20;
        """,
        '3': """
            select p.Data_Jogo as Data_,
                   e1.Apelido as Mandante,
                   e2.Apelido as Visitante,
                   p.Pts_Casa as Pontos_Mandante,
                   p.Pts_Visit as Pontos_Visitante,
                   (p.Pts_Visit - p.Pts_Casa) as Diferenca
            from (Equipe e1, Equipe e2) join (
                                            select ID_Time_Mandante,
                                                   ID_Time_Visitante,
                                                   Pts_Casa,
                                                   Pts_Visit,
                                                   Data_Jogo
                                            from Jogo
                                            where Pts_Visit - Pts_Casa > 30
                                            ) as p
            on (e1.ID_Time, e2.ID_Time) = (p.ID_Time_Mandante, p.ID_Time_Visitante)
            order by Diferenca desc
            limit 10;
        """,
        '4': """
            select e.Cidade,
                   e.Apelido,
                   Mais_Venceram_Casa.Num_Jogos
            from Equipe e join (
                                select ID_Time_Mandante,
                                       count(ID_Jogo) as Num_Jogos
                                from Jogo
                                where Time_Casa_Vence is true
                                group by ID_Time_Mandante
                            ) as Mais_Venceram_Casa
            on Mais_Venceram_Casa.ID_Time_Mandante=e.ID_Time
            order by Num_Jogos desc limit 10;
        """,
        '5': """
            with Desempenho_Temporada as (
                select ID_Temporada,
                       max(Data_Ranking) as Data_Ranking,
                       max(Vitorias) as Max_Vitorias
                from Ranking
                where ID_Temporada >= 22004 and ID_Temporada <= 22021
                group by ID_Temporada
            )

            select e.Cidade,
                   e.Apelido,
                   r.ID_Temporada,
                   r.Vitorias
            from Equipe e natural join Ranking r
            where (r.ID_Temporada, r.Data_Ranking, r.Vitorias) = (
                                                                select *
                                                                from Desempenho_Temporada dt
                                                                where dt.ID_Temporada = r.ID_Temporada and
                                                                      dt.Data_Ranking = r.Data_Ranking and
                                                                      dt.Max_Vitorias = r.Vitorias
                                                                )
            order by r.ID_Temporada limit 10;
        """,
        '6': """
            with ID_Num_Temporadas as
                (select ID_Jogador as ID,
                        count(distinct Temporada) as Num_Temporadas,
                        count(distinct ID_Time) as Num_Times
                from Joga_Em
                group by ID_Jogador)

            select j.Nome, intemp.Num_Temporadas, intemp.Num_Times
            from Jogador j left outer join ID_Num_Temporadas intemp
            on j.ID_Jogador = intemp.ID
            order by intemp.Num_Temporadas desc, intemp.Num_Times desc limit 10;
        """
    }
    query = queries.get(query_number, '')
    if query:
        results = query_db(query)
        return render_template('results.html', results=results, query_number=query_number)
    else:
        return "Consulta inválida", 400

if __name__ == '__main__':
    app.run(debug=True)
