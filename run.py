from APP import create_app

app = create_app()

#Run Server... runing on Port 5000#
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
