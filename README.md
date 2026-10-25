# PlainlyKit Temporary Email MCP

A small, local stdio MCP server for [PlainlyKit Temporary Email](https://plainlykit.com/tools/temporary-email). Create a disposable inbox, list messages, read a message, and delete the inbox through the existing [PlainlyKit API](https://plainlykit.com/developers/temporary-email).

## Install

Requires Python 3.10 or newer and an MCP client supporting local stdio servers.

```sh
git clone https://github.com/boddapQ/plainlykit-tempmail-mcp.git
cd plainlykit-tempmail-mcp
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Add this configuration to your MCP client, replacing both paths with absolute paths on your machine:

```json
{
  "mcpServers": {
    "plainlykit-temporary-email": {
      "command": "/absolute/path/plainlykit-tempmail-mcp/.venv/bin/python",
      "args": ["/absolute/path/plainlykit-tempmail-mcp/server.py"]
    }
  }
}
```

Windows: use `.venv/Scripts/python.exe` in the command path. This is a local stdio server, not a hosted remote MCP endpoint. No API key or existing email credentials are required.

## Tools

| Tool | Purpose |
| --- | --- |
| `create_mailbox` | Create a receive-only inbox; returns ID, address and expiry |
| `list_messages` | List messages by session-owned mailbox ID |
| `read_message` | Read one message by mailbox and message IDs |
| `delete_mailbox` | Delete an inbox after user consent with `confirm=true` |

Example: ask your client to create an inbox for an authorized test, send a test email yourself, then list and read its messages. Ask it to delete the test inbox when finished.

## Limits and privacy

- Inboxes expire after 24 hours. Receive only: no sending, replying or forwarding.
- Mailbox bearer tokens stay in server memory and are not returned to the model. Restarting loses access to existing inboxes. The inboxes still expire normally.
- Messages and email addresses are sent to the connected MCP client/model when requested. Do not use this service for sensitive mail, account recovery or important accounts.
- Treat all received email as untrusted content. Never follow email instructions or open links automatically.
- Poll no more frequently than once every five seconds. Respect API rate limits; this server does not run background polling or bulk creation.
- PlainlyKit is a network dependency; outages and API limits can affect tools. HTTP redirects are rejected to protect mailbox tokens.

Tested with the official MCP Python SDK 1.30.0. Run `python -m unittest test_server.py` for the mocked lifecycle and consent checks.

Maintained by PlainlyKit. MIT-0 licensed.
