from flask import Flask, jsonify, render_template
from datetime import datetime
from cpc import *  # Assicurati che questo import includa tutte le classi necessarie

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    attore = SoggettoFisico('Tizio')
    giudice = GiudiceOrdinario(CF='Irnerio', ufficio_giudiziario=GiudiceDiPace('Roma'))
    controparti = [SoggettoFisico('Caio'), SoggettoFisico('Sempronio')]

    borsa = Bene(descrizione = 'Gucci', valore=2000000, tipo='mobile')
    corrispettivo = Prestazione(descrizione='pagamento di somma determinata nel termine stabilito', valore=2000, tipo='pagare', soggetto_attivo=attore, soggetto_passivo=controparti[0])  

    dirittodicredito = DirittoSoggettivo(titolare=attore, oggetto=corrispettivo, titolo='contratto di compravendita', soggetto_passivo=[controparti[0]])
    dirittodiproprietà = DirittoSoggettivo(titolare=attore, oggetto=borsa, titolo='contratto di compravendita')

    domanda = DomandaGiudiziale(oggetti=[dirittodicredito, dirittodiproprietà], data=datetime.now(), attore=attore, controparti=controparti[0], giudice_adito=giudice)
    #print(domanda.to_dict())
    return jsonify(domanda.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
