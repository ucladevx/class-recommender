// TODO figure out why home.scss can't be resolved. I get an error whenever I try to load it in. 

//import 'home.scss';
import React from 'react';
import {connect} from 'react-redux';

import Config from 'config';

import Subjects from 'subjects';
import SubjectDropdown from './subject_dropdown';
import ClassDropdown from './class_dropdown';


// This home.js file will serve as the home page for the class scanner portion of the project

class DropdownParent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {propsForClassDropdown: []};
    this.inputClasses = this.inputClasses.bind(this);
  }

  inputClasses(list){
      console.log("get classes:");
      console.log(list);
       console.log(this.state);
      this.setState({propsForClassDropdown:[]});
      this.setState({propsForClassDropdown: this.state.propsForClassDropdown.concat(list)});
     
  }


  render(){
    return(
    <div className = "DropdownContainer">
      <SubjectDropdown triggerListChange ={(classList)=>this.inputClasses(classList)} />
      <ClassDropdown />
    </div>
    )
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

export default DropdownParent;
