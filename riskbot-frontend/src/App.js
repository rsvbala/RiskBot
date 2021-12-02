
import React from 'react';
import Widget from 'rasa-webchat';


function App() {

  // useEffect(() => {
  //   const newSocket = io(`http://localhost:5005`);
  //   setSocket(newSocket);
  //   return () => newSocket.close();
  // }, [setSocket]);
  //
  // console.log(socket)
  return (
    <div className="App">
      <Widget
        initPayload={"/greet"}
        socketUrl={"http://127.0.0.1:5005"}
        socketPath={"/socket.io/"}
        customData={{"language": "en"}}
        title={"RiskBot"}
        subTitle={"Support"}
      />
    </div>
  );
}

export default App;
