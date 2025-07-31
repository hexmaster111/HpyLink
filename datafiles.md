
# data header
| size     | use           |
| -------- | ------------- |
| 4 bytes  | channel count |
| 32 bytes | reserved      |

# data body

| size             | use              |
| ---------------- | ---------------- |
| 8                | relitive time    |
| channelcount * 8 | data for channel |

This then repets to EOF
