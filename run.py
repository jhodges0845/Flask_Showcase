from APP import create_app

hodges-flask-showcase = create_app()

#Run Server Debug... runing on Port 5000#
#Run Server Production... runing on Port 80#
if __name__ == '__main__':
    hodges-flask-showcase.run(host='0.0.0.0', port='80')
