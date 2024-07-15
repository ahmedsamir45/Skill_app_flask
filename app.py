from webapp import create_app



app = create_app()






    

if __name__ == "__main__" :
    app.run(debug=False,port=5000,host="0.0.0.0")


    #flaskapp\Scripts\activate
    # pip install Flask-SQLAlchemy==2.5.1
    # with app.app_context():
    #     db.create_all()