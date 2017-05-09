import React from 'react';
import {connect} from 'react-redux';


class Scans extends React.Component {
  render(){
    return <div>
      Scans<br/>
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


Scans = connect(mapStateToProps, mapDispatchToProps)(Scans);
export default Scans
