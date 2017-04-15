import React from 'react';
import {connect} from 'react-redux';

import Config from 'config';


class Home extends React.Component {
  render(){
    return <div>
      {Config.info.msg}<br/>
      Path: {this.props.urlPath}<br/>
      <button onClick={()=>{test()}}>Print This</button>


    </div>;
  }
}

function test() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
             console.log(this.responseText);
        }
    };
    xhttp.open("GET", "http://localhost:5000", true);
    xhttp.send();
}


const mapStateToProps = (state)=>{
  return {
    urlPath: state.router.location.pathname,
  };
};

const mapDispatchToProps = (dispatch)=>{
  return {
    printlog: (input)=>{
      console.log(input);
      // dispatch(action);
    },
  };
};


Home = connect(mapStateToProps, mapDispatchToProps)(Home);
export default Home
