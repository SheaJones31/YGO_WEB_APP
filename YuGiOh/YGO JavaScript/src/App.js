import React from 'react';
import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      cards: [],
      currentCards: [],
      loadingCards: [],  // keep track of which cards are currently loading
    };
  }

  componentDidMount() {
    fetch('http://localhost:5000/')
      .then(response => response.json())
      .then(data => this.setState({cards: data}));
  }

  getCardDetails(cardId) {
    const existingCardIndex = this.state.currentCards.findIndex(card => card.id === cardId);

    if (existingCardIndex > -1) {
      // If the card is already displayed, remove it
      this.setState(prevState => {
        const updatedCards = [...prevState.currentCards];
        updatedCards.splice(existingCardIndex, 1);
        return { currentCards: updatedCards };
      });
    } else {
      // add card to loadingCards
      this.setState(prevState => ({ loadingCards: [...prevState.loadingCards, cardId] }));

      // Fetch and show new card
      fetch(`http://localhost:5000/${cardId}`)
        .then(response => response.json())
        .then(data => {
          this.setState(prevState => {
            // remove card from loadingCards and add to currentCards
            const loadingCards = prevState.loadingCards.filter(id => id !== cardId);
            return { currentCards: [...prevState.currentCards, data], loadingCards };
          });
        });
    }
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          {this.state.cards.map((card, index) => (
            <div key={index}>
              <h2 onClick={() => this.getCardDetails(card.id)}>{card.name}</h2>
              {this.state.loadingCards.includes(card.id) ? (
                <p>Loading...</p>
              ) : (
                <div>
                  {this.state.currentCards.map((currentCard) => {
                    if (currentCard.id === card.id) {
                      return (
                        <div key={currentCard.id}>
                          <p>Name: {currentCard.name}</p>
                          <p>Type: {currentCard.type}</p>
                          <p>Attribute: {currentCard.attribute}</p>
                          {/* Add other card details as you see fit */}
                        </div>
                      );
                    }
                    return null;
                  })}
                </div>
              )}
            </div>
          ))}
        </header>
      </div>
    );
  }
}

export default App;