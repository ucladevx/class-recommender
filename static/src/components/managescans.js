import React from 'react';
import {connect} from 'react-redux';


class ManageScans extends React.Component {
  render(){
    return <div>
      ManageScans<br/>
      Path: {this.props.urlPath}
    </div>;
  }
}

const mapStateToProps = (state)=>{
  return {
    urlPath: state.router.location.pathname,
  };
};

const mapDispatchToProps = (dispatch)=>{
  return {
  };
};


ManageScans = connect(mapStateToProps, mapDispatchToProps)(ManageScans);
export default ManageScans
