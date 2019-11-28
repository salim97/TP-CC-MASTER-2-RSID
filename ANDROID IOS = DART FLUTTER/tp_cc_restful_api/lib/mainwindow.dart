import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class MainWindow extends StatefulWidget {
  MainWindow({Key key}) : super(key: key);

  @override
  _MainWindowState createState() => _MainWindowState();
}

class _MainWindowState extends State<MainWindow> {
  int _cIndex = 0;

@override
  void initState() {
    // TODO: implement initState
    super.initState();
    ipController.text ="192.168.1.11" ;
  }
  void _incrementTab(index) {
    setState(() {
      _cIndex = index;
    });
  }

  String ip = null;
  @override
  Widget build(BuildContext context) {
    if (ip == null) {
      return Scaffold(
          appBar: AppBar(
            title: Text("TP CC MASTER 2 RSID"),
          ),
          body: Column(
              mainAxisAlignment: MainAxisAlignment.center,
  crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.all(18.0),
                child: TextFormField(
                  decoration: InputDecoration(
                    labelText: "IP",
                  ),
                  keyboardType: TextInputType.text,
                  controller: ipController,
                ),
              ),
              RaisedButton(
                onPressed: () async {
                  setState(() {
                    ip = ipController.text;
                  });
                },
                child: Text("Save IP of server ( default port = 2019 )"),
              ),
            ],
          ));
    }
    return Scaffold(
        resizeToAvoidBottomInset: false,
        appBar: AppBar(
          title: Text("TP CC MASTER 2 RSID"),
        ),
        body: _cIndex == 0 ? page01() : page02(),
        floatingActionButton: _cIndex == 1
            ? FloatingActionButton(
                child: Icon(Icons.refresh),
                onPressed: () async {
                  final response = await http.get('http://admin:admin@'+ip+':2019/user/list');
                  setState(() {
                    bodyResponse3 = response.body;
                  });
                },
              )
            : Container(),
        bottomNavigationBar: BottomNavigationBar(
          currentIndex: _cIndex,
          //type: BottomNavigationBarType.shifting ,
          items: [
            BottomNavigationBarItem(icon: Icon(Icons.grid_on), title: new Text('Prime number')),
            BottomNavigationBarItem(icon: Icon(Icons.supervised_user_circle), title: new Text('Admin')),
          ],
          onTap: (index) {
            _incrementTab(index);
          },
        ));
  }

  final userInputController = TextEditingController();
  final ipController = TextEditingController();
  String bodyResponse = "", bodyResponse2 = "", bodyResponse3 = "";
  Widget page01() {
    return Column(
      children: <Widget>[
        Padding(
          padding: const EdgeInsets.all(18.0),
          child: TextFormField(
            decoration: InputDecoration(
              labelText: "Enter number to print all prime number below it",
            ),
            keyboardType: TextInputType.number,
            controller: userInputController,
          ),
        ),
        RaisedButton(
          onPressed: () async {
            if(userInputController.text.isEmpty) return ;
            final uri = 'http://'+ip+':2019/prime/' + userInputController.text;
            var map = new Map<String, dynamic>();
            map['userName'] = 'admin';
            map['password'] = 'admin';

            http.Response response = await http.post(
              uri,
              body: map,
            );
            print("----------------------");
            print(response.body);
            setState(() {
              bodyResponse = response.body;
            });
          },
          child: Text("Send request to backend"),
        ),
        Divider(),
        Padding(
          padding: const EdgeInsets.all(18.0),
          child: Text(bodyResponse),
        )
      ],
    );
  }

  final usernameController = TextEditingController();
  final passwordController = TextEditingController();

  Widget page02() {
    return Column(
      children: <Widget>[
        Padding(
          padding: const EdgeInsets.all(18.0),
          child: TextFormField(
            decoration: InputDecoration(
              labelText: "new user name",
            ),
            keyboardType: TextInputType.text,
            controller: usernameController,
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(18.0),
          child: TextFormField(
            decoration: InputDecoration(
              labelText: "new password",
            ),
            keyboardType: TextInputType.text,
            controller: passwordController,
          ),
        ),
        RaisedButton(
          onPressed: () async {
            final uri = 'http://admin:admin@'+ip+':2019/user/add';
            var map = new Map<String, dynamic>();
            map['userName'] = usernameController.text;
            map['password'] = passwordController.text;
            http.Response response = await http.post(
              uri,
              body: map,
            );
            print("----------------------");
            print(response.body);
            setState(() {
              bodyResponse2 = response.body;
            });
          },
          child: Text("Add new user"),
        ),
        Divider(),
        Padding(
          padding: const EdgeInsets.all(18.0),
          child: Text(bodyResponse2),
        ),
        Divider(),
        Padding(
          padding: const EdgeInsets.all(18.0),
          child: Text(bodyResponse3),
        )
      ],
    );
  }
}
