#!/bin/bash

# Start the first process
/bin/ollama serve &

# Start the second process
streamlit run streamlit_app.py --server.port 80

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
