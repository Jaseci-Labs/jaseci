node Doc {
  has text;
  has entities;
  has intents;
}
node Chunk{
  has text;
}
node Intent{
  has name;
  has count;
}
node Entity{
  has name;
  has count;
}

// Definition of nodes

edge PredefIntent;
edge PredefEntity;
edge Root2Doc;
edge Belong;

graph createGraphTest {
    has anchor testRoot;
    spawn {
        testRoot = spawn node::root;
    }
}

graph segmenterTest {
    has anchor testRoot;
    spawn {
        testRoot = spawn node::root;
        // testIntent = spawn node::Intent(name="Education", count=0);
        // testRoot -[PredefIntent]-> testIntent;
        testIntent = spawn testRoot -[PredefIntent]-> node::Intent(name="Education", count=0);
        testEntity = spawn testRoot -[PredefEntity]-> node::Entity(name="Michigan", count=0);
    }
}

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
    entities = ['Michigan', 'University', 'Jaseci', 'Ann Arbor'];
    // List all the predefined entities here.
  }
}
walker createPredefines {
  // This walker creates all the predefined elements attached to root including intents and entitites.
  root {
    intents = spawn here walker::getIntents;
    // Create all the intents
    for intent in intents {
      spawn here -[PredefIntent]-> node::Intent(name = intent, count = 0);
    }
    // Create all the entities
    entities = spawn here walker::getEntities;
    for entity in entities{
      spawn here -[PredefEntity]-> node::Entity(name = entity, count = 0);
    }
  }
}

walker segmenter {
  // This walker creates the segment nodes of a documentation
  has entities, intents;
  can text_segmentor.get_segments;
  root {
    doc = spawn here -[Root2Doc]-> node::Doc;
    entities = -[PredefEntity]->;
    intents = -[PredefIntent]->;
    take -[Root2Doc]->;
  }
  Doc {
    segs =['The University of Michigan is a university located in Ann Arbor.', 'The University of Michigan is recognized as one of the best engineering schools in US.', 'I like coding Jaseci in University of Michigan.'];
    here.text = 'The University of Michigan is a university located in Ann Arbor. It is recoginized as one of the best engineering schools in US. I like coding Jaseci in University of Michigan.';
    segs = text_segmentor.get_segments(text = here.text, threshold = 0.95);
    std.out(segs);
    // Please call the AI model API here instead.
    for i in segs{
      segNode = spawn here --> node::Chunk(text = i);
      spawn segNode walker::entityExtractor(entities = entities);
      spawn segNode walker::intentExtractor(intents = intents);
    }
  }
}

walker entityExtractor {
  // The walker creates entity links based on the given segment (Chunk)
  has entities;
  can ent_ext.entity_detection;
  Chunk {
    // chunkEntities = ["Michigan", "Dream", "Jaseci"];
    // Definitely CALL THE AI HERE!!
    entityExtraction = ent_ext.entity_detection(text = here.text)['entities']; 
    // This is the list of entities detect by the AI model.
    for entity in entityExtraction {
      for entityNode in entities {
        if (entityNode.name == entity['entity_text']){
          here -[Belong]-> entityNode;
          entityNode.count += 1;
        }
      }
    }
  }
}

walker intentExtractor {
  has intents;
  Chunk {
    chunkIntents = ["Education"];
    for intentNode in intents {
      if (intentNode.name in chunkIntents) {
        here -[Belong]-> intentNode;
        intentNode.count += 1;
      }
    }
  }
}

walker getAnswer {
    // This walker returns the answer of the given intent and entities
    has intentName, entityName;
    has res;
    root {
        intentName = '';
        entityName = 'Jaseci';
        take -[PredefIntent]->;
        take -[PredefEntity]->;
    }
    Intent {
        std.out('Intent Node Answer');
        res = [];
        if (intentName == here.name) {
            for seg in <-[Belong]- {
                res = res + [seg.text];
            }
        }
        report res;
    }
    Entity {
        res = [];
        if (entityName == here.name) {
            for seg in <-[Belong]- {
                res = res + [seg.text];
            }
        }
        report res;
    }
}

test "test initializer"
with graph::createGraphTest by walker::createPredefines {
    count = 0;
    for i in -[PredefIntent]-> {
        count = count + 1;
    }
    for i in spawn here walker::getIntents {
        count = count - 1;
    }
    assert count == 0;

    for i in -[PredefEntity]-> {
        count = count + 1;
    }
    for i in spawn here walker::getEntities {
        count = count - 1;
    }
    assert count == 0;
}

test "test segmenter"
with graph::segmenterTest by walker::segmenter{
    count = 0;
    for i in --> {
        count = count + 1;
    }
    std.out(count);
    assert count == 2; //There should be 3 segments
}

test "test intentExtractor"
with graph::segmenterTest by walker::segmenter{
    for i in intents {
        std.out(i.count);
        assert i.count == 2;
    }
}
test "test entityExtractor"
with graph::segmenterTest by walker::segmenter{
    for i in entities {
        std.out(i.count);
        assert i.count == 0;
    }
}
