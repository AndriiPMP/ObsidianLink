# ObsidianLinks

ObsidianLinks is a project created to make life easier for people who manually create connections between their notes and manually organize everything into folders.

The main goal of ObsidianLinks is to automate this process using local embedding AI models. The application analyzes your Obsidian notes, finds semantically related files, and automatically connects them using standard Obsidian links.

It can also help sort notes into folders, reducing the amount of manual work needed to keep an Obsidian vault clean and well-organized.

## Features

- Automatic semantic search between notes
- Local embedding AI models
- Automatic creation of Obsidian-compatible links
- Folder-based note sorting
- TUI interface for easier interaction
- Works with an existing Obsidian vault
- Redis and MongoDB / MongoDB Atlas support

## How It Works

ObsidianLinks uses local embedding models to understand the meaning of your notes.  
Instead of matching only exact words, it searches for notes that are connected by meaning and context.

After finding related notes, ObsidianLinks automatically adds links between them using standard Obsidian link syntax.

This helps create a more connected knowledge base without manually searching through files and adding links one by one.

## Requirements

Before running the project, make sure you have:

- Python installed
- Docker installed
- Redis running
- MongoDB Atlas configured, or a local MongoDB instance for development
- An existing Obsidian vault

## Environment Configuration

Before starting the application, configure the `.env` file.

The most important value is `BASE_DIR`, which should point to the current location of your Obsidian vault.

Example:

```env
BASE_DIR=/path/to/your/obsidian/vault
