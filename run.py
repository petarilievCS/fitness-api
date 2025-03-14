from app import create, db

app = create()

if __name__=="__main__":
    with app.app_context():
        db.create_all() 
        print("Database created successfully!")
    app.run(debug=True)
