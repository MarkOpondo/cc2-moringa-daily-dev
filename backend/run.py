from app import create_app

# Passes 'development' as the config_name
app = create_app(config_class="development")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)