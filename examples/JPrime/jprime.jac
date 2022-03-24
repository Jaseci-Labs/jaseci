node Doc {
  has text;
  has entities;
  has intents;
}
node Chunk{
  has text;
  has entities;
  has intents;
}
node Intent{
  has name;
}
node Entity{
  has name;
}

// Definition of nodes

edge PredefIntent;
edge PredefEntity;
edge Root2Doc;

walker getIntents {
  // This walker always returns the predefined getIntents
  has anchor intents;
  with entry {
    intents = ['Movies', 'Education', 'Food', 'Cars', 'Music'];
  }
}


walker getEntities {
  // This walker always returns the predefined entities
  has anchor entities;
  with entry {
    entities = ['Michigan', 'University', 'Jaseci' ];
    // List all the predefined entities here.
  }
}
walker createPredefines {
  // This walker creates all the predefined elements attached to root including intents and entitites.
  root {
    intents = spawn here walker::getIntents;
    // Create all the intents
    for intent in intents {
      spawn here -[PredefIntent]-> node::Intent(name = intent);
    }
    // Create all the entities
    entities = spawn here walker::getEntities;
    for entity in entities{
      spawn here -[PredefEntity]-> node::Entity(name = entity);
    }
  }
}

walker segmenter {
  // This walker creates the segment nodes of a documentation
  has entities, intents;
  root {
    doc = spawn here -[Root2Doc]-> node::Doc;
    entities = -[PredefEntity]->;
    intents = -[PredefIntent]->;
    take -[Root2Doc]->;
  }
  Doc {
    segs =['The University of Michigan is a university located in Ann Arbor.', 'The University of Michigan is recognized as one of the best engineering schools in US.', 'I like coding Jaseci in University of Michigan.'];
    // Please call the AI model API here instead.

    for i in segs{
      segNode = spawn here --> node::Chunk(text = i, entities = entities, intents = intents);
      spawn segNode walker::entityExtractor(entites = entities);
      spawn segNode walker::intentExtractor(entites = entities);
    }
  }
}

walker entityExtractor {
  // The walker creates entity links based on the given segment (Chunk)
  has entities;
  Chunk {
    chunkEntities = ["Michigan", "Dream", "Jaseci"];
    // Definitely CALL THE AI HERE!!
    for entityNode in here.entities {
      std.out(entityNode.name);
      if (entityNode.name in chunkEntities){
        here --> entityNode;
      }
    }
  }
}

walker intentExtractor {
  Chunk {
    chunkIntents = ["Education"];
    for intentNode in here.intents {
      if (intentNode.name in chunkIntents) {
        here --> intentNode;
      }
    }
  }
}