# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

```
Steps to implement retrieve(query, n_results):

Check if the collection is empty:

If _collection.count() returns 0, there’s nothing to retrieve, so return an empty list.
Query the collection:

Use _collection.query() to perform the semantic search with the given query.
Extract results:

Since the query results are nested lists, extract the first query's results using [0].
Format the results:

Combine the documents, metadatas, and distances into a list of dictionaries.
Return the results:

Return the formatted list of relevant chunks.
```

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```
[your answer here]
```

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

```
Example of _collection.query() Result
{
    "documents": [
        [
            "Chunk text 1",
            "Chunk text 2",
            "Chunk text 3"
        ]
    ],
    "metadatas": [
        [
            {"game": "Game A"},
            {"game": "Game B"},
            {"game": "Game A"}
        ]
    ],
    "distances": [
        [
            0.12,
            0.34,
            0.45
        ]
    ]
}
# Extract the first query's results
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
```

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

```
I would only return the first one since the retrieve() function is designed to handle only one query at a time, we access the first result using [0] to extract the relevant data for that single query.
```

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

```
A: return an empty list when colletion is empty
B: Results will still be returned, but the distances will be high, indicating poor matches
C: The _collection.query() method will return chunks from all relevant games, as long as they are among the top n_results based on similarity scores
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query: What happens if you roll a 7 in Catan?
Top result game: Catan
Distance score: 0.47089511156082153
Chunk text: x, that hex produces no resources that turn, regardless of the number rolled.

ROLLING A 7
When a 7 is rolled, no resources are produced. Every player with more than 7 resource cards in hand must discard half (rounded down). The player who rolled moves the robber to any terrain hex and steals one ra
Does it make sense? Yes
```

**One thing about the query results that surprised you:**

```
when I clicked "What happens if you roll a 7 in Catan?" button on site, it returned "Response generation not yet implemented. Complete Milestone 3 to activate answers."
```
