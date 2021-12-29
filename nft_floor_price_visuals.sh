#!/bin/bash

# Run this to grant permisions: in terminal: chmod 700 {filename}

source ~/.bash_profile;
cd ~/Projects; source .env/bin/activate;
cd ~/Projects/NFT/OpenSea;
python3 nft_floor_price_visuals.py;
