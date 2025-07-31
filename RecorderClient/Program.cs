

using System.Net;
using System.Net.Sockets;

int port = 0;
string server = "";
IPAddress ep;

if (args.Length != 3)
{
    Usage();
    return 1;
}

if (!int.TryParse(args[1], out port))
{
    Console.WriteLine($"{args[1]} is not a valid port.");
    Usage();
    return 1;
}

server = args[0];
ep = IPAddress.Parse(server);
string outfile = args[2];

var f = File.Create(outfile);


Console.WriteLine($"Connecting to {ep}:{port}...");
Socket client = new(ep.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
client.Connect(ep, port);

Console.WriteLine($"Connected !");

var channelCountBytes = new byte[4];

int got = client.Receive(channelCountBytes);

if (got != channelCountBytes.Length)
{
    Console.WriteLine("Didnt get enough data to be a valid channel counts.");
    return 1;
}
var channelCounts = BitConverter.ToUInt32(channelCountBytes);
Console.WriteLine($"Server has {channelCounts} channels / frame");

var expectedBytes = (channelCounts + 1) * sizeof(double);
bool run = true;

f.Write(channelCountBytes);
f.Write(new byte[32]); // save the reserved space in the file with nothing

DateTime nextDisplayUpdate = DateTime.Now;
ulong samplesGot = 0;

try
{
    while (run)
    {
        var sampleBytes = new byte[expectedBytes];
        got = client.Receive(sampleBytes);

        if (got != expectedBytes) throw new Exception("Oopse, that packet was short.... Guess i do have to handle this");

        f.Write(sampleBytes);
        samplesGot += 1;

        if (Console.KeyAvailable)
        {
            var k = Console.ReadKey();
            if (k.Key == ConsoleKey.Escape) run = false;
        }

        if (DateTime.Now > nextDisplayUpdate)
        {
            nextDisplayUpdate = DateTime.Now + TimeSpan.FromMilliseconds(500);

            Console.Clear();
            Console.WriteLine($"got {samplesGot} samples");
            Console.WriteLine($"Runtime: {BitConverter.ToDouble(sampleBytes, 0):0.000} s");  // first sample is time from start
        }

    }
}
catch (Exception ex)
{
    Console.WriteLine(ex);
    Console.WriteLine("Shutting down due to error");
}



f.Close();
Console.WriteLine("Shutting down...");

client.Shutdown(SocketShutdown.Both);
client.Close();

Console.WriteLine("Disconnected");
return 0;

void Usage()
{
    Console.WriteLine("./RecorderClient server port output_file_name.dat");
}
