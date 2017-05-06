import React from 'react';
import {connect} from 'react-redux';

import Config from 'config';
import 'bootstrap-sass'
// This home.js file will serve as the home page for the class scanner portion of the project

class Home extends React.Component {
  render(){
    return
    <div>
      {Config.info.msg}<br/>
      Path: {this.props.urlPath}<br/>
      <button onClick={()=>{test()}}>Print dThissds</button>
        <select>
          <option>Summer Session A - 2017</option>
          <option>Summer Session B - 2017</option>
          <option>Summer Session C - 2017</option>
      </select>
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
    xhttp.open("GET", "http://localhost:8000", true);
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
