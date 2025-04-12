# Makefile for P2P File Sharing System

.PHONY: all clean run-tracker run-peers run-alice run-bob

# Default target
all: help

# Help target
help:
	@echo "P2P File Sharing System"
	@echo ""
	@echo "Available commands:"
	@echo "  make run-all     - Run all components in the correct order"
	@echo "  make run-tracker - Run the tracker server"
	@echo "  make run-peers   - Run all peer servers"
	@echo "  make run-alice   - Run Alice (file sharing)"
	@echo "  make run-bob     - Run Bob (file retrieval)"
	@echo "  make clean       - Clean up generated files and directories"
	@echo ""
	@echo "Individual peer commands:"
	@echo "  make run-peer1   - Run peer server 1"
	@echo "  make run-peer2   - Run peer server 2"
	@echo "  make run-peer3   - Run peer server 3" 
	@echo "  make run-peer4   - Run peer server 4"

# Run the tracker server
run-tracker:
	@echo "Starting Tracker Server..."
	@python tracker_server.py

# Run individual peer servers
run-peer1:
	@echo "Starting Peer Server 1..."
	@python peer_server1.py 8001

run-peer2:
	@echo "Starting Peer Server 2..."
	@python peer_server2.py 8002

run-peer3:
	@echo "Starting Peer Server 3..."
	@python peer_server3.py 8003

run-peer4:
	@echo "Starting Peer Server 4..."
	@python peer_server4.py 8004 

# Run all peer servers (requires multiple terminals)
# Note: In practice, you'll want to run each peer in a separate terminal
run-peers:
	@echo "Please run each peer server in a separate terminal using:"
	@echo "  make run-peer1"
	@echo "  make run-peer2"
	@echo "  make run-peer3"
	@echo "  make run-peer4"

# Run Alice (file sharing)
run-alice:
	@echo "Starting Alice (File Sharing)..."
	@python alice.py

# Run Bob (file retrieval)
run-bob:
	@echo "Starting Bob (File Retrieval)..."
	@python bob.py

# Run all components (this is informational as running them in a single process won't work properly)
run-all:
	@echo "The components need to be run in separate terminals in this order:"
	@echo "1. make run-tracker"
	@echo "2. make run-peer1 (in a separate terminal)"
	@echo "3. make run-peer2 (in a separate terminal)"
	@echo "4. make run-peer3 (in a separate terminal)"
	@echo "5. make run-peer4 (in a separate terminal)"
	@echo "6. make run-alice"
	@echo "7. make run-bob"

run-peers-mac: run-peer1 run-peer2 run-peer3 run-peer4

run-all-mac: run-tracker run-peers
	@osascript -e 'tell application "Terminal" to do script "cd $(PWD) && sleep 3 && python3 alice.py"'
	@osascript -e 'tell application "Terminal" to do script "cd $(PWD) && sleep 6 && python3 bob.py"'

# Clean up generated files and directories
clean:
	@echo "Cleaning up..."
	@rm -rf chunks
	@rm -rf peer_8001_chunks
	@rm -rf peer_8002_chunks
	@rm -rf peer_8003_chunks
	@rm -rf peer_8004_chunks
	@rm -rf bob_received_chunks
	@rm -f bob_received_file.txt
	@echo "Clean up complete!"

