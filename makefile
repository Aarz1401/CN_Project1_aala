
share:
	python file_sharer.py

peers:
	python peer.py peer1 &
	python peer.py peer2 &
	python peer.py peer3 &

retrieve:
	python file_retriever.py

clean:
	rm -rf peer_data chunks reconstructed_file.txt
	-pkill -f file_sharer.py || true
	-pkill -f peer.py || true
