// TODO figure out why home.scss can't be resolved. I get an error whenever I try to load it in. 

//import 'home.scss';
import React from 'react';
import {connect} from 'react-redux';

import Config from 'config';
import Dropdown from 'react-dropdown'
import {DropdownButton, ButtonGroup, Button, MenuItem} from 'react-bootstrap'
import SearchInput, {createFilter} from 'react-search-input'
import Subjects from 'subjects'

const KEYS_TO_FILTERS = ['subject.name']

// This home.js file will serve as the home page for the class scanner portion of the project

class SubjectDropdown extends React.Component {
  constructor(props) {
    super(props);
    this.state = { searchTerm: "", searchStarted: false };
    this.searchUpdated = this.searchUpdated.bind(this);
  }
  searchUpdated (term) {
    this.setState({searchTerm: term, searchStarted: true})
  }

  onItemClick(item, e) {  
    this.props.triggerListChange(item.subject);
  }

  render(){
    const filteredSubjects = Subjects.filter(createFilter(this.state.searchTerm, KEYS_TO_FILTERS))
    return(
    <div>
      <div className = "SubjectDropdownContainer">
        <SearchInput className='search-input' onChange={this.searchUpdated} />
            <div className = 'SubjectDropdown'>
              {filteredSubjects.map(Subjects => {
                  let itemClick = this.onItemClick.bind(this, Subjects);
                  return (
                    <div className = "dropdownItem" key={Subjects.id} onClick={itemClick}>
                      {Subjects.subject.name}
                    </div>
                  )
              })}
            </div>
      </div>
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

export default SubjectDropdown;
