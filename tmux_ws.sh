#!/bin/sh

# Set Session Name
SESSION="Scraper"
SESSIONEXISTS=$(tmux list-sessions | grep $SESSION)

# Only create tmux session if it doesn't already exist
if [ "$SESSIONEXISTS" = "" ]
then
    # Start New Session with our name
    tmux new-session -d -s $SESSION

    # Name first Pane and start Main
    tmux rename-window -t 0 'Main'
    tmux send-keys -t 'Main' 'vim botscraper/bot/telegram.py' C-m
    tmux split-window -h
    tmux send-keys -t 'Main' 'vim botscraper/core/scraper.py' C-m
    tmux split-window -h
    tmux split-window -v
    tmux send-keys -t 'Main' 'watch -n 2 systemctl status botscraper' C-m
    tmux select-pane -L
    tmux split-window -v
    tmux send-key -t 'Main' 'vim botscraper/scrapers/pci.py' C-m
    tmux select-pane -L

    # Create and setup pane for Debug
    tmux new-window -t $SESSION:1 -n 'Debug'
    tmux send-keys -t 'Hugo Server' 'hugo serve -D -F' C-m # Switch to bind script?
fi

# Attach Session, on the Main window
tmux attach-session -t $SESSION:0
