import React, { Component } from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Amplify, {API,graphqlOperation} from 'aws-amplify';
import { withAuthenticator, Authenticator, Greetings} from 'aws-amplify-react';
import { createTodo, deleteTodo } from "./graphql/mutations"
import { listTodos } from "./graphql/queries"
import aws_exports from './aws-exports'; // specify the location of aws-exports.js file on your project
Amplify.configure(aws_exports);

class App extends Component {
  //create initial state
  state = {name: '', date: '', description: '', hours: '', todos: [] }
  
  //update state when user types into inputs
  onChange = event => {
    this.setState({ [event.target.name]: event.target.value })
  }

  // list current entries
  async listNotes(){
    const todos = await API.graphql(graphqlOperation(listTodos));
    this.setState({ todos: todos.data.listTodos.items })
  }

  //update entries in gui
  async componentDidMount() {
    try {
      const todos = await API.graphql(graphqlOperation(listTodos))
      console.log('showing todos: ', todos)
      this.setState({ todos: todos.data.listTodos.items })
    } catch (err) {
      console.log('error fetching data: ', err)
    }
  }
  
  // create enrties
  CreateTodo = async() => {
    if (
      this.state.name === '' ||
      this.state.date === '' || 
      this.state.description === '' || 
      this.state.hours === ''
    ) return
    try {
      const todo = { 
        name: this.state.name, 
        date: this.state.date, 
        description: this.state.description,
        hours: this.state.hours 
      }
      const variables = {
        input: todo, // key is "input" based on the mutation above
      };
      
      const todos = [...this.state.todos, todo]
      this.setState({ name: '', date: '', description: '' , hours: '', todos })
      await API.graphql(graphqlOperation(createTodo, variables))
      console.log('todo successfully created!', todo)
      this.listNotes();
    } catch (err) {
      console.log('error creating todo ...', err)
    }
  }

  // Delete entries 
  DeleteTodo = async(id)  => {
    try{
      const input = { id: id }
      const result = await API.graphql(graphqlOperation(deleteTodo, { input }))
      console.log('todo successfully deleted!', { result })
      this.listNotes();
    } catch (err) {
      console.log('error deleting todo ...', err)
    }
	}

  //render the component
  render() {
    const data = [].concat(this.state.todos).map((item,i)=> 
      <div className="alert alert-primary alert-dismissible show" role="alert">
        <span key={item.i}>
          Name: {item.name} Datum: {item.date} Elternarbeit: {item.description} Stunden: {item.hours} 
        </span>
        <button 
          key={item.i} 
          type="button" 
          className="close" 
          data-dismiss="alert" 
          aria-label="Close" 
          onClick={this.DeleteTodo.bind(this, item.id)}>
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      )
    return (
      <div className="App">
                <Authenticator hideDefault={true}>
            <Greetings
                inGreeting={(username) => 'Du bist eingelogt als ' + username + '!'}
            />
        </Authenticator>
        <div className="container">
          <legend>Trag' deine Elternstunden in das Formular ein.</legend>
            <form>
              <p>
                <input id="name" type="text" placeholder="Name" className="form-control" value={this.state.name} onChange={this.onChange} name='name' />
              </p>
              <p>
                <input id="date" type="text" placeholder="Datum der Elternarbeit" className="form-control" value={this.state.date} onChange={this.onChange} name='date' />
              </p>
              <p>
              <input id="description" type="text" placeholder="Beschreibung der Elternarbeit" className="form-control" value={this.state.description} onChange={this.onChange} name='description' />
              </p>
              <p>
                <input id="hours" type="number" placeholder="Anzahl Elternstunden" className="form-control" value={this.state.hours} onChange={this.onChange} name='hours' />
              </p>
              <button type="submit" className="btn btn-primary" onClick={this.CreateTodo}>Eintrag vornehmen</button>
            </form>
        </div>
        <hr></hr>
        <div className="container">
          <legend>Erfasste Elternstunden</legend>
          <p>Falsch erfasste Stunden bitten löschen und neu eintragen.</p>
            {data}
        </div>
        <hr></hr>
      </div>

    )
  }
}

export default withAuthenticator(App, {
  signUpConfig: {
    hiddenDefaults: ["phone_number"],
    signUpFields: [
      { label: "Familienname", key: "name", required: true, type: "string" }
    ]
  }
});