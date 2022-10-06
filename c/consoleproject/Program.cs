using System;
using System.Web;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using WebSocketSharp;
using Newtonsoft.Json;

namespace ConsoleApp {
    class Program {
        static void Main(string[] args) {
            using (var ws = new WebSocket("ws://10.192.61.160:9876/socket.io/?EIO=4&transport=websocket")) {
                var exitEvent = new ManualResetEvent(false);

                // ws.MessageReceived.Subscribe(msg => Console.WriteLine($"msg.Text: {msg.Text},  msg.MessageType: {msg.MessageType}"));

                ws.OnMessage += (sender, e) => {
                    string response = e.Data;
                    Console.WriteLine("RESPONSE: " + response);
                    // Console.WriteLine("SENDING MESSAGE..");
                    // Console.WriteLine(ServerMessage);
                    // ws.Send(ServerMessage);
                };
                ws.OnError += (sender, e) => {
                    Console.WriteLine("ERROR: " + e.Message);
                };

                ws.OnClose += (sender, e) => {
                    Console.WriteLine("CLOSED!");
                };

                ws.OnOpen += (sender, e) => {
                    Console.WriteLine("CONNECTED!");
                };


                Console.WriteLine("CONNECTING..");
                ws.Connect();

                Console.ReadKey(true);
            }
        }
    }
}
