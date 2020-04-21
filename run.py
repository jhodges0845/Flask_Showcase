from APP import create_app

app = create_app()

#Run Server Debug... runing on Port 5000#
#Run Server Production... runing on Port 80#
if __name__ == '__main__':
    app.run(host='0.0.0.0')
