# %% LIBRERIE
from typing import Union, List, Optional
from datetime import datetime
import json

# %% [markdown]
# Nel principio Iddio creò i cieli e la terra. E la terra era informe e vuota, e le tenebre coprivano la faccia dell’abisso, e lo spirito di Dio aleggiava sulla superficie delle acque. E Dio disse: Sia la luce! E la luce fu. E Dio vide che la luce era buona; e Dio separò la luce dalle tenebre. E Dio chiamò la luce "giorno", e le tenebre "notte". Così fu sera, poi fu mattina: e fu il primo giorno.

# %% NOZIONI
""" Art. 1. 

 (Capacità giuridica). 

 La capacità giuridica si acquista dal momento della nascita. 

 I diritti che la legge riconosce a favore del concepito sono subordinati all'evento della nascita. 

((IL D.LGS. LUOGOTENENZIALE 14 SETTEMBRE 1944, N. 287 HA CONFERMATO L'ABROGAZIONE DEL PRESENTE COMMA)).  """
class Soggetto:
    """ Rappresenta un soggetto generico con un Codice Fiscale. """
    
    def __init__(self, CF: str):
        if not CF:
            raise ValueError("Il Codice Fiscale non può essere vuoto.")
        self.CF = CF

    def __str__(self) -> str:
        return self.CF

    def to_dict(self) -> dict:
        """ Restituisce una rappresentazione dizionario del Soggetto. """
        return {'CF': self.CF}

class SoggettoFisico(Soggetto):
    """ Rappresenta un soggetto fisico, estendendo Soggetto con un attributo di residenza. """

    def __init__(self, CF: str, residenza: str = None):
        super().__init__(CF)
        self.residenza = residenza if residenza is not None else "Non specificata"

    def __str__(self) -> str:
        return f'{self.CF}, Residenza: {self.residenza}'

    def to_dict(self) -> dict:
        """ Includi la residenza nella rappresentazione dizionario. """
        base_dict = super().to_dict()
        base_dict['residenza'] = self.residenza
        return base_dict

class SoggettoGiuridico(Soggetto):
    """ Rappresenta un soggetto giuridico con una sede legale. """

    def __init__(self, CF: str, sede: str = "Non specificata"):
        super().__init__(CF)
        self.sede = sede

    def __str__(self) -> str:
        return f'{self.CF}, Sede: {self.sede}'

    def to_dict(self) -> dict:
        """ Includi la sede nella rappresentazione dizionario. """
        base_dict = super().to_dict()
        base_dict['sede'] = self.sede
        return base_dict


""" Art. 810. codice civile

 (Nozione). 

 Sono beni le cose che possono formare oggetto di diritti. 
 """
class Bene:
    """ Rappresenta un bene con descrizione, tipo e valore.
        Tipi includono 'mobile', 'immobile', 'immateriale', e 'giuridico' come default.
    """
    
    def __init__(self, descrizione: str, tipo: str = "giuridico", valore: int = None):
        if not descrizione:
            raise ValueError("La descrizione del bene non può essere vuota.")
        self._descrizione = descrizione
        self._tipo = tipo
        self._valore = valore if valore is not None else 0  # Assumi 0 se non specificato

    @property
    def descrizione(self):
        return self._descrizione

    @property
    def tipo(self):
        return self._tipo

    @property
    def valore(self):
        return self._valore

    @valore.setter
    def valore(self, valore):
        if valore is not None and valore < 0:
            raise ValueError("Il valore del bene non può essere negativo.")
        self._valore = valore

    def __str__(self):
        return f"{self.descrizione}, Valore: {self.valore}, Tipo: {self.tipo}"

    def to_dict(self):
        """ Restituisce una rappresentazione dizionario del Bene. """
        return {
            'descrizione': self.descrizione,
            'valore': self.valore,
            'tipo': self.tipo
        }

""" Art. 1173. codice civile

 (Fonti delle obbligazioni). 

 Le obbligazioni derivano da contratto, da fatto illecito, o da ogni altr atto o fatto idoneo a produrle in conformità dell'ordinamento giuridico. 

Art. 1174. codice civile

 (Carattere patrimoniale della prestazione). 

 La prestazione che forma oggetto dell'obbligazione deve essere suscettibile di valutazione economica e deve corrispondere a un interesse, anche non patrimoniale, del creditore

Art. 1175. codice civile

 (Comportamento secondo correttezza). 

 Il debitore e il creditore devono comportarsi secondo le regole della correttezza, ((...)).

 """
class Prestazione:
    """ Rappresenta una prestazione, con descrizione, valore monetario, tipo, e soggetti attivi e passivi coinvolti. """

    def __init__(self, descrizione: str, valore: int, tipo: str, 
                 soggetto_attivo: Union['SoggettoFisico', 'SoggettoGiuridico', List[Union['SoggettoFisico', 'SoggettoGiuridico']]], 
                 soggetto_passivo: Union['SoggettoFisico', 'SoggettoGiuridico', List[Union['SoggettoFisico', 'SoggettoGiuridico']]]):
        if not descrizione:
            raise ValueError("La descrizione non può essere vuota.")
        if valore < 0:
            raise ValueError("Il valore non può essere negativo.")
        
        self.descrizione = descrizione
        self.valore = valore
        self.tipo = tipo
        self.soggetto_attivo = soggetto_attivo
        self.soggetto_passivo = self._ensure_list(soggetto_passivo)

    @staticmethod
    def _ensure_list(soggetto):
        """ Assicura che il soggetto sia una lista, indipendentemente dal fatto che sia stato fornito come singolo oggetto o come lista. """
        return soggetto if isinstance(soggetto, list) else [soggetto]

    def __str__(self):
        passivi = ', '.join(sp.CF for sp in self.soggetto_passivo)
        return f"{self.descrizione}, Valore: {self.valore}, Tipo: {self.tipo}, Soggetto passivo: {passivi}"

    def to_dict(self):
        """ Restituisce una rappresentazione dizionario dell'oggetto, includendo i soggetti passivi serializzati. """
        return {
            'descrizione': self.descrizione,
            'valore': self.valore,
            'tipo': self.tipo,
            'soggetto_passivo': [sp.to_dict() for sp in self.soggetto_passivo]
        }



# %% ORDINAMENTO GIURIDICO
class Ordinamento:
    """ Rappresenta il sistema giuridico specifico di un territorio con una data cittadinanza. """

    def __init__(self, territorio: str = 'italiano', cittadinanza: str = 'italiana', time: datetime = None):
        if not territorio or not cittadinanza:
            raise ValueError("Territorio e cittadinanza devono essere specificati.")
        
        self.territorio = territorio
        self.cittadinanza = cittadinanza
        self.time = time if time else datetime.now()

    def __str__(self):
        return f"Repubblica {self.cittadinanza} del popolo {self.territorio}"

    def to_dict(self):
        """ Restituisce una rappresentazione dizionario dell'oggetto, includendo timestamp della creazione. """
        return {
            'territorio': self.territorio,
            'cittadinanza': self.cittadinanza,
            'time': self.time.isoformat()
        }
# %% DIRITTO SOSTANZIALE
from typing import Union

from typing import Union, List

class DirittoSoggettivo:
    """ Rappresenta un diritto soggettivo con attributi dettagliati quali titolare, oggetto, natura, categoria e pretese legali. """

    def __init__(self, titolare: Union['SoggettoFisico', 'SoggettoGiuridico'], 
                 oggetto: Union['Bene', 'Prestazione'],  
                 ordinamento_giuridico: Ordinamento = Ordinamento(territorio='Italiano', cittadinanza='italiana'),
                 soggetto_passivo: List[Union['SoggettoFisico', 'SoggettoGiuridico', str]] = None,  
                 titolo: str = 'legge'):
        self.titolare = titolare
        self.oggetto = oggetto
        self.ordinamento_giuridico = ordinamento_giuridico
        self.titolo = titolo
        self.soggetto_passivo = soggetto_passivo if isinstance(soggetto_passivo, list) else ([soggetto_passivo] if soggetto_passivo else [])
        self.categoria = self.determina_categoria()
        self.natura = self.determina_natura()
        self.valore = self.get_valore()
        self.pretesa = self.determina_pretesa()

    def get_valore(self):
        """ Restituisce il valore monetario dell'oggetto se disponibile. """
        return self.oggetto.valore if hasattr(self.oggetto, 'valore') and self.oggetto.valore is not None else 0

    def determina_natura(self):
        """ Determina se il diritto è patrimoniale o non patrimoniale basato sul valore. """
        natura = 'patrimoniale' if self.get_valore() > 0 else 'non patrimoniale'
        return ('relativo', natura) if self.soggetto_passivo else ('assoluto', natura)

    def determina_categoria(self):
        """ Categorizza il diritto basato sul tipo di oggetto. """
        if isinstance(self.oggetto, Bene):
            return ('reale', 'di godimento' if self.soggetto_passivo else 'di proprietà')
        elif isinstance(self.oggetto, Prestazione):
            return ('di credito',)
        return ('non specificata',)

    def determina_pretesa(self):
        """ Costruisce una descrizione della pretesa legale basata sul diritto e la sua natura. """
        pretesa = []
        if isinstance(self.oggetto, Bene) and self.categoria[0] == 'reale':
            pretesa.append(self.format_pretesa_bene())
        elif isinstance(self.oggetto, Prestazione) and self.categoria[0] == 'di credito':
            pretesa.append(self.format_pretesa_prestazione())
        return tuple(pretesa)

    def format_pretesa_bene(self):
        """ Formatta la pretesa per i beni reali. """
        if self.categoria[1] == 'di proprietà' and self.natura[0] == 'assoluto':
            return f'godimento e disposizione pieno e indisturbato di {self.oggetto.descrizione}'
        elif self.categoria[1] == 'di godimento':
            passivi_desc = ', '.join(sp.CF for sp in self.soggetto_passivo)
            return f'godimento limitato di {self.oggetto.descrizione} con {passivi_desc} secondo {self.titolo}'

    def format_pretesa_prestazione(self):
        """ Formatta la pretesa per le prestazioni di credito. """
        passivi_desc = ', '.join(sp.CF for sp in self.soggetto_passivo)
        return f'prestazione di {self.oggetto.descrizione} dovuta da {passivi_desc} come stabilito da {self.titolo}'

    def __str__(self):
        oggetto_desc = str(self.oggetto)
        categoria_desc = ', '.join(self.categoria)
        natura_desc = ', '.join(self.natura)
        passivi = ', '.join([sp.CF for sp in self.soggetto_passivo])
        return (f"Diritto {natura_desc} {categoria_desc} di {self.titolare}\n"                
                f"Oggetto: {oggetto_desc}\n"
                f"Pretesa: {self.pretesa}\n"
                f"Titolo: {self.titolo}\n\n"
                f"Soggetti Passivi: {passivi}\n"
                f"Ordinamento Giuridico: {self.ordinamento_giuridico.territorio}\n")
        
    def to_dict(self):
        """ Serializza l'oggetto in un dizionario per facilitare la serializzazione JSON. """
        return {
            'natura': self.natura,
            'categoria': self.categoria,
            'titolare': self.titolare.to_dict() if hasattr(self.titolare, 'to_dict') else str(self.titolare),
            'pretesa': self.pretesa,
            'oggetto': self.oggetto.to_dict() if hasattr(self.oggetto, 'to_dict') else str(self.oggetto),
            'soggetti_passivi': [sp.to_dict() for sp in self.soggetto_passivo],
            'titolo': self.titolo,
            'valore': self.valore,
            'ordinamento_giuridico': {'territorio': self.ordinamento_giuridico.territorio}
        }

class InteresseLegittimo:
    pass

# %% [markdown] REGIO DECRETO 30 gennaio 1941, n. 12
# 

# %% PM

""" Art. 2.

(Del pubblico ministero).

Presso la corte di cassazione, le corti di appello, i tribunali ordinari e i tribunali per i minorenni è costituito l'ufficio del pubblico ministero.(109)((110a))
 """
 
class PubblicoMinistero(SoggettoFisico):
    """
    Rappresenta un Pubblico Ministero, una figura giuridica che opera nel sistema giudiziario,
    estendendo le proprietà di un Soggetto Fisico con specifiche funzionalità e responsabilità legali.
    """

    def __init__(self, CF: str, ufficio: str = "Non specificato"):
        super().__init__(CF)
        self.ufficio = ufficio  # Ufficio in cui il Pubblico Ministero opera

    def __str__(self) -> str:
        return f"Pubblico Ministero {self.CF}, Residenza: {self.residenza}, Ufficio: {self.ufficio}"

    def to_dict(self) -> dict:
        """
        Restituisce una rappresentazione dizionario dell'oggetto, includendo tutte le proprietà
        ereditate e quelle specifiche del Pubblico Ministero.
        """
        base_dict = super().to_dict()  # Otteniamo il dizionario dalla classe base
        base_dict['ufficio'] = self.ufficio  # Aggiungiamo il campo ufficio
        return base_dict

def costituisci_PM(**args):
    if args:
        return PubblicoMinistero(**args)
    else:
        return PubblicoMinistero('test')

# %% UFFUCI GIUDIZIARI
""" 
Art. 1.

Dei giudici.

La giustizia nelle materie civile e penale è amministrata:
a) dal giudice di pace;
b) ((LETTERA SOPPRESSA DAL D.LGS. 19 FEBBRAIO 1998, N. 51)); ((110a))
c) dal tribunale ordinario;
d) dalla corte di appello;
e) dalla Corte di cassazione;
f) dal tribunale per i minorenni;
g) dal megistrato di sorveglianza;
h) dal tribunale di sorveglianza; (106a) """

class GiudiceDiPace:
    """Rappresenta un giudice di pace, operante in un dato territorio."""
    def __init__(self, territorio: str = 'Roma'):
        self.territorio = territorio

    def __str__(self):
        return f"Giudice di Pace in {self.territorio}"

    def to_dict(self):
        return {'territorio': self.territorio}

class Tribunale:
    """Rappresenta un tribunale ordinario, che può avere diverse sezioni."""
    def __init__(self, territorio: str = 'Roma', sezione: Optional[str] = None):
        self.territorio = territorio
        self.sezione = sezione or 'Ordinaria'
        self.PM = costituisci_PM() 

    def __str__(self):
        return f"Tribunale di {self.territorio}, Sezione: {self.sezione}, PM: {self.PM}"

    def to_dict(self):
        return {'territorio': self.territorio, 'sezione': self.sezione, 'PM': self.PM.to_dict()}


class CortedAppello:
    def __init__(self, sezione, territorio='Roma'):
        self.territorio = territorio
        self.sezione = sezione
        self.PM = costituisci_PM()
        
    def __str__(self):
        return f"Corte d'Appello di {self.territorio}, Sezione: {self.sezione}, PM: {self.PM}"

    def to_dict(self):
        return {'territorio': self.territorio, 'sezione': self.sezione, 'PM': self.PM}

class CortediCassazione:
    def __init__(self, sez_unite=False, sezione=None):
        self.sezioni_unite = sez_unite
        self.sezione = sezione if sezione else 'Generale'
        self.PM = costituisci_PM()

    def __str__(self):
        return f"Corte di Cassazione, Sezioni Unite: {self.sezioni_unite}, Sezione: {self.sezione}, PM: {self.PM}"

    def to_dict(self):
        return {'sezioni_unite': self.sezioni_unite, 'sezione': self.sezione, 'PM': self.PM}

class TribunaleperiMinorenni:
    def __init__(self, territorio='Roma'):
        self.territorio = territorio
        self.PM = costituisci_PM()

    def __str__(self):
        return f"Tribunale per i Minorenni di {self.territorio}, PM: {self.PM}"

    def to_dict(self):
        return {'territorio': self.territorio, 'PM': self.PM}

class MagistratodiSorveglianza:
    def __init__(self, territorio='Roma'):
        self.territorio = territorio

    def __str__(self):
        return f"Magistrato di Sorveglianza di {self.territorio}"

    def to_dict(self):
        return {'territorio': self.territorio}

class TribunalediSorveglianza:
    def __init__(self, territorio='Roma'):
        self.territorio = territorio

    def __str__(self):
        return f"Tribunale di Sorveglianza di {self.territorio}"

    def to_dict(self):
        return {'territorio': self.territorio}

class GiudiceOrdinario(SoggettoFisico):
    def __init__(self, CF: str, ufficio_giudiziario: Union[GiudiceDiPace, Tribunale, CortedAppello, PubblicoMinistero, CortediCassazione, TribunaleperiMinorenni, TribunalediSorveglianza, MagistratodiSorveglianza]):
        super().__init__(CF)  # Passiamo il CF al costruttore della superclasse
        self.ufficio_giudiziario = ufficio_giudiziario
        
    def to_dict(self):
        # Ricaviamo il dizionario base da SoggettoFisico
        giudice_dict = super().to_dict()
        # Aggiungiamo il campo ufficio_giudiziario, che dovrà avere un proprio metodo to_dict()
        giudice_dict['ufficio_giudiziario'] = self.ufficio_giudiziario.to_dict() if hasattr(self.ufficio_giudiziario, 'to_dict') else str(self.ufficio_giudiziario)
        return giudice_dict

    

# %% [markdown] REGIO DECRETO 28 ottobre 1940, n. 1443 - CPC
# 
# LIBRO PRIMO - DISPOSIZIONI GENERALI
#     TITOLO I - DEGLI ORGANI GIUDIZIARI
#         CAPO I - Del giudice
#                Sezione I - Della giurisdizione e della competenza in generale

# %% DOMANDA
class DomandaGiudiziale:
    """ Rappresenta una domanda giudiziale con diversi elementi legali, la data di presentazione, il richiedente, il giudice adito, e le controparti. """

    def __init__(self, oggetti: List[Union['DirittoSoggettivo', 'InteresseLegittimo']], 
                 data: datetime, 
                 attore: Union['SoggettoFisico', 'SoggettoGiuridico'], 
                 giudice_adito: GiudiceOrdinario, 
                 controparti: List[Union['SoggettoFisico', 'SoggettoGiuridico']] = None):
        
        if not all(isinstance(oggetto, (DirittoSoggettivo, InteresseLegittimo)) for oggetto in oggetti):
            raise ValueError("L'oggetto della domanda deve essere una pretesa tutelata dall'ordinamento!")
        
        self.oggetti = oggetti
        self.data = data
        self.attore = attore
        self.controparti = self._ensure_list(controparti)
        self.valore = self.get_valore()
        self.giudice_adito = giudice_adito
    
    @staticmethod
    def _ensure_list(soggetto):
        """ Assicura che il soggetto sia una lista, indipendentemente dal fatto che sia stato fornito come singolo oggetto o come lista. """
        return soggetto if isinstance(soggetto, list) else [soggetto]


    def get_valore(self):
        """ Calcola il valore totale della domanda basato sulla natura patrimoniale dei diritti soggettivi coinvolti. """
        return sum(oggetto.valore for oggetto in self.oggetti if isinstance(oggetto, DirittoSoggettivo) and 'patrimoniale' in oggetto.natura)

    def __str__(self):
        oggetti_desc = ', '.join(oggetto.to_dict()['descrizione'] for oggetto in self.oggetti)
        return (f"Domanda presentata il {self.data.strftime('%d/%m/%Y')} da {self.attore} contro {', '.join(str(c) for c in self.controparti)}, "
                f"comprendente i seguenti diritti: {oggetti_desc}. Valore totale: €{self.valore}")

    def to_dict(self):
        """ Serializza l'oggetto in un dizionario per facilitare la serializzazione JSON. """
        return {
            'oggetti': [oggetto.to_dict() for oggetto in self.oggetti],
            'data': self.data.isoformat(),
            'attore': self.attore.to_dict() if hasattr(self.attore, 'to_dict') else str(self.attore),
            'controparti': [cp.to_dict() for cp in self.controparti] if self.controparti else [],
            'valore': self.valore,
            'giudice_adito': self.giudice_adito.to_dict() if hasattr(self.giudice_adito, 'to_dict') else str(self.giudice_adito)
        }




# %% GIURISDIZIONE 
class GiurisdizioneOrdinaria:
    
    """ Art. 5. 
    (Momento determinante della giurisdizione e della competenza). 

    La giurisdizione e la competenza si determinano con riguardo alla legge vigente e allo stato di fatto esistente al momento della proposizione della domanda, e non hanno rilevanza rispetto ad esse i successivi mutamenti della legge o dello stato medesimo. 
        """
    def __init__(self, ordinamento: Ordinamento = Ordinamento(), domande: List[DomandaGiudiziale] = None, giudice: GiudiceOrdinario = None):
        self.ordinamento = ordinamento
        self.domande = domande if domande else print('Ubi non est actio, ibi non est iurisdictio')
        self.giudice = giudice if giudice else print('Art. 1. \n (Giurisdizione dei giudici ordinari).\n La giurisdizione civile, salvo speciali disposizioni di legge, è esercitata dai giudici ordinari secondo le norme del presente codice.\n ')
        self.timestamp = self.ordinamento.time
        self.giurisdizione = [self.check_giurisdizione(domanda) for domanda in self.domande] if self.domande else self.check_giurisdizione()
        self.competenza = [self.check_competenza(domanda=domanda) for domanda in self.domande] if self.domande else self.check_competenza()


            
    def check_giurisdizione(self, domanda:DomandaGiudiziale = None):
        if domanda:
            if all(hasattr(oggetto, 'ordinamento_giuridico') for oggetto in domanda.oggetti):
                if all(oggetto.ordinamento_giuridico.territorio == self.ordinamento.territorio for oggetto in domanda.oggetti):
                    return True, f'Giurisdizione presente - Giurisdizione ordinaria ({self.ordinamento.cittadinanza})'
                else:
                    ordinamenti = set(oggetto.ordinamento_giuridico.cittadinanza for oggetto in domanda.oggetti)
                    eccezioni = [ordinamento for ordinamento in ordinamenti if ordinamento != self.ordinamento.territorio]
                    return False, f'Difetto assoluto di giurisdizione - Giurisdizione estera ({", ".join(eccezioni)})'
            else:
                return False, 'Difetto assoluto di giurisdizione - Giurisdizione inesistente'
        return False, 'Ubi non est actio, ibi non est iurisdictio'


   
    """ Art. 6. 
        (Inderogabilità convenzionale della competenza). 

        La competenza non può essere derogata per accordo delle parti, salvo che nei casi stabiliti dalla legge. 
    """
    
    def check_competenza(self, accordo = False, domanda:DomandaGiudiziale = None):
        competenza = []
       
        if domanda and (hasattr(domanda, 'giudice_adito') and domanda.giudice_adito != None):
            valore = domanda.valore
            beni = [oggetto for oggetto in domanda.oggetti if isinstance(oggetto.oggetto, Bene)]
            prestazioni = [oggetto for oggetto in domanda.oggetti if isinstance(oggetto.oggetto, Prestazione)]
            
            """  Art. 7.
        
            (Competenza del giudice di pace).

            Il giudice di pace è competente per le cause relative a beni mobili di valore non superiore a diecimila euro, quando dalla legge non sono attribuite alla competenza di altro giudice. (171) ((173))
            Il giudice di pace è altresì competente per le cause di risarcimento del danno prodotto dalla circolazione di veicoli e di natanti, purché il valore della controversia non superi venticinquemila euro. (171) ((173))

            E' competente qualunque ne sia il valore:
            1) per le cause relative ad apposizione di termini ed osservanza delle distanze stabilite dalla legge, dai regolamenti o dagli usi riguardo al piantamento degli alberi e delle siepi;
            2) per le cause relative alla misura ed alle modalità d'uso dei servizi di condominio di case;
            3) per le cause relative a rapporti tra proprietari o detentori di immobili adibiti a civile abitazione in materia di immissioni di fumo o di calore, esalazioni, rumori, scuotimenti e simili propagazioni che superino la nomale tollerabilità;
            3-bis) per le cause relative agli interessi o accessori da ritardato pagamento di prestazioni previdenziali o assistenziali;
            (72) """
        
            art7c1_1 = all(bene.oggetto.tipo == 'mobile' for bene in beni) if beni else False
            
            art7c1_2 = any(
                'risarcimento' in prestazione.oggetto.descrizione.lower() and
                any(term in prestazione.oggetto.descrizione.lower() for term in ['autoveicoli', 'natanti'])
                for prestazione in prestazioni
            )
            
            art7c2 = any(
                any(term in prestazione.oggetto.descrizione.lower() for term in ['termini', 'distanze', 'immissioni', 'servizi di condominio', 'previdenziali'])
                for prestazione in prestazioni
            )
            
            """ Art. 9.
            (Competenza del tribunale).
            Il tribunale è competente per tutte le cause che non sono di competenza di altro giudice.
            Il tribunale è altresì esclusivamente competente per le cause in materia di imposte e tasse, per quelle relative allo stato e alla capacità delle persone e ai diritti onorifici, per la querela di falso, per l'esecuzione forzata e, in generale, per ogni causa di valore indeterminabile
            """   
            
            art9c2 = any(
            any(term in prestazione.oggetto.descrizione.lower() for term in ['imposta', 'tassa', 'status', 'capacità', 'querela di falso', 'esecusione forzata'])
            for prestazione in prestazioni
                )
            
            if (valore < 10000 and art7c1_1) or (valore < 25000 and art7c1_2) or art7c2:
                competenza =  [GiudiceDiPace()]    
            elif art9c2:
                competenza = [Tribunale()] 
            else:
                competenza = [Tribunale()]
            
            if self.giudice == domanda.giudice_adito:
                if type(domanda.giudice_adito.ufficio_giudiziario) == type(competenza[0]):
                    self.competenza = (True, domanda.giudice_adito)
                    return True, f"Competenza confermata di {domanda.giudice_adito}"
                else:
                    self.competenza = (False, self.RegolamentodiCompetenza())
                    return False, f"Incompetenza rilevata, indicazione della competenza..."
            elif self.giudice != domanda.giudice_adito:
                if type(self.giudice.ufficio_giudiziario) == type(competenza[0]):
                    self.competenza = (True, self.giudice)
                    return True, f"Competenza confermata di {self.giudice}"
                else:
                    self.competenza = (False, self.RegolamentodiCompetenza())
                    return False, f"Giudice procedente {self.giudice} incompetente! Regolamento necessario (competenza prevista: {competenza[0]})"

        else:
            self.competenza = (False, 'Ubi non est actio, ibi non est iurisdictio') 
            return False, 'Ubi non est actio, ibi non est iurisdictio'
        
    def RegolamentodiCompetenza(self):
        pass
    
    def __str__(self):
            domande_str = ', '.join([str(domanda) for domanda in self.domande])
            return f"Ordinamento: {self.ordinamento}, Domande: {domande_str}, Giudice: {self.giudice}, " \
                f"Timestamp: {self.timestamp}, Giurisdizione: {self.giurisdizione}, Competenza: {self.competenza}"

    def to_dict(self):
        """ Serializza l'oggetto per facilitare la memorizzazione o la trasmissione. """
        return {
            "ordinamento": str(self.ordinamento),
            "domande": [domanda.to_dict() for domanda in self.domande],
            "giudice": str(self.giudice) if self.giudice else None,
            "timestamp": self.timestamp.isoformat(),
            "giurisdizione": [g.to_dict() for g in self.giurisdizione],
            "competenza": [c.to_dict() for c in self.competenza]
        }

# %% MAIN
""" ordinamento_ita = Ordinamento(territorio='italiano')
ordinamento_de = Ordinamento(territorio='tedesco', cittadinanza='tedesca')
TribuRoma = Tribunale(territorio='Roma')
GdPRoma = GiudiceDiPace(territorio='Roma')

giudice1 = GiudiceOrdinario(SoggettoFisico('Irnerio'), ufficio_giudiziario=TribuRoma)
giudice2 = GiudiceOrdinario(SoggettoFisico('Accursio'), ufficio_giudiziario=GdPRoma)

attore = SoggettoFisico('Tizio')
controparti = [SoggettoFisico('Caio'), SoggettoFisico('Sempronio')]

villa = Bene(descrizione ='villa', valore = 10000, tipo='immobile')

orologio = Bene(descrizione = 'Rolex', valore=199900, tipo='mobile')
borsa = Bene(descrizione = 'Gucci', valore=2000000, tipo='mobile')

corrispettivo = Prestazione(descrizione='pagamento di somma determinata nel termine stabilito', valore=2000, tipo='pagare', soggetto_attivo=attore, soggetto_passivo=controparti[0])  

dirittodicredito = DirittoSoggettivo(titolare=attore, oggetto=corrispettivo, titolo='contratto di compravendita', ordinamento_giuridico=ordinamento_ita)
dirittodiproprietà = DirittoSoggettivo(titolare=attore, oggetto=borsa, titolo='contratto di compravendita', ordinamento_giuridico=ordinamento_ita)

domanda = DomandaGiudiziale(oggetti=[dirittodicredito, dirittodiproprietà], data=datetime.now(), attore=attore, controparte=controparti[0], giudice_adito=giudice1)
iurisdictio = GiurisdizioneOrdinaria(ordinamento=ordinamento_ita, domande=[domanda], giudice=giudice1)

#print(f'----- DIRITTO 1 -----  \n {dirittodicredito} \n\n ----- DIRITTO 2 -----  \n {dirittodiproprietà} \n \n {iurisdictio}')



 """