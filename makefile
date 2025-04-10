

share:
	python file_sharer.py

tracker:
	@echo " Starting tracker on port 5000..."
	python tracker.py &

peers:
	@echo " Starting peers..."
	python peer.py peer1 &
	python peer.py peer2 &
	python peer.py peer3 &

retrieve:
	python file_retriever.py

clean:
	@echo " Cleaning up..."
	-rm -rf peer_data chunks reconstructed_file.txt tracker_db.json
	-pkill -f peer.py || true
	-pkill -f tracker.py || true
