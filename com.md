# Server client protocal
1. client connects to server
2. server sends channel count
3. client sends "OK"
4. server starts streaming data out


# Starting the client
> dotnet run 127.0.0.1 54359 datafile.dat
- in the RecorderClient
