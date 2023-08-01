import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# create the app
app = Flask(__name__)
app.app_context().push()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///assignment3.db"
# initialize the app with the extension
db.init_app(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    countryName = db.Column(db.String, nullable=False)
    offName = db.Column(db.String, nullable=False)
    nativeName = db.Column(db.String, nullable=False)
    currenciesName = db.Column(db.String, nullable=False)
    curSymbol = db.Column(db.String, nullable=False)
    capital = db.Column(db.String, nullable=False)
    region = db.Column(db.String, nullable=False)
    subregion = db.Column(db.String, nullable=False)
    languages = db.Column(db.String, nullable=False)
    population = db.Column(db.String, nullable=False)
    area = db.Column(db.String, nullable=False)
    flags = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    try:
        print(request.values['country'])
        country = request.values['country']
        url = f'https://restcountries.com/v3.1/name/{country}'
        r = requests.get(url)
        data = r.json()[0]
        officialhr = data['name']['official']
        official = data['name']['nativeName']
        offcc = ''
        offc = []
        for c, d in official.items():
            for j, b in d.items():
                offc.append(b)
        for i in range(len(offc)):
            offcc = offcc + offc[0]
            break
        flagg = data['flags']['png']
        currencies = data['currencies'][list(data['currencies'].keys())[0]]['name']
        symb = data['currencies'][list(data['currencies'].keys())[0]]['symbol']
        capital = data['capital'][0]
        region = data['region']
        subreg = data['subregion']
        langd = data['languages']
        langls = []
        langst = ''
        for k, v in langd.items():
            langls.append(v)
        for i in range(len(langls)):
            if (len(langls) == 1):
                langst = langst + langls[i]
            elif (i == 0):
                langst = langst + langls[i] + ', ' + langls[i + 1]
            elif (i > 1):
                langst = langst + ', ' + langls[i]
        population = data['population']
        s = data['area']
        def quer():
            f = []
            for i in user.query.all():
                f.append(i.countryName)
            return f
        if r.status_code == 200:
            user1 = user(countryName = f"{data['name']['common']}",
                         offName = f"{officialhr}",
                         nativeName = f"{offcc}",
                         currenciesName = f"{currencies}",
                         curSymbol = f"{symb}",
                         capital = f"{capital}",
                         region = f"{region}",
                         subregion = f"{subreg}",
                         languages = f"{langst}",
                         population = f"{population}",
                         area = f"{s}",
                         flags = f"{flagg}")
            key = '6ae37b61afb6ad1033a5747eb164a39b'
            weurl = f'https://api.openweathermap.org/data/2.5/weather?q={capital}&appid={key}&units=metric'
            getw = requests.get(weurl)
            dataw = getw.json()
            apiweather = dataw['main']['temp']
            iconn = dataw['weather'][0]['icon']
            if(any(f"{data['name']['common']}" in datas for datas in quer())):
                return render_template('country.html',
                                       weathe=apiweather,
                                       weathericon = iconn,
                                       offici=user1.offName,
                                       png=user1.flags,
                                       ofic_name=user1.nativeName,
                                       curr=user1.currenciesName,
                                       symbol=user1.curSymbol,
                                       capCity=user1.capital,
                                       reg=user1.region,
                                       subr=user1.subregion,
                                       languages=user1.languages,
                                       population=user1.population,
                                       area=user1.area)
            else:
                db.session.add(user1)
                db.session.commit()
    except KeyError:
        return render_template('error.html')
    return render_template('country.html',
                           weathe=apiweather,
                           weathericon=iconn,
                           offici=user1.offName,
                           png=user1.flags,
                           ofic_name=user1.nativeName,
                           curr=user1.currenciesName,
                           symbol=user1.curSymbol,
                           capCity=user1.capital,
                           reg=user1.region,
                           subr=user1.subregion,
                           languages=user1.languages,
                           population=user1.population,
                           area=user1.area)

if __name__ == '__main__':
    app.run(debug=True)