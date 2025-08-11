## Instructions for Using Graphiti's MCP Tools for Agent Memory

### Before Starting Any Task

- **Always search first:** Use the `search_nodes` tool to look for relevant preferences and procedures before beginning work.
- **Search for facts too:** Use the `search_facts` tool to discover relationships and factual information that may be relevant to your task.
- **Filter by entity type:** Specify `Preference`, `Procedure`, or `Requirement` in your node search to get targeted results, or use custom types for your domain.
- **Review all matches:** Carefully examine any preferences, procedures, or facts that match your current task.

### Always Save New or Updated Information

- **Capture requirements and preferences immediately:** When a user expresses a requirement or preference, use `add_memory` to store it right away.
  - _Best practice:_ Split very long requirements into shorter, logical chunks.
- **Be explicit if something is an update to existing knowledge.** Only add what's changed or new to the graph.
- **Document procedures clearly:** When you discover how a user wants things done, record it as a procedure.
- **Record factual relationships:** When you learn about connections between entities, store these as facts.
- **Be specific with categories:** Label preferences and procedures with clear categories for better retrieval later.

### CRITICAL: Protected Attributes Rules

**STOP! Before defining ANY custom entity, check this list:**

<protected-attributes>
uuid, name, group_id, labels, created_at, name_embedding, summary, attributes
</protected-attributes>

**RULE: If your entity field matches ANY word above, you MUST use a different field name.**

**VALIDATION CHECKLIST:**
1. Does your field name equal "name"? → Use "title", "label", or domain-specific term
2. Does your field name equal "uuid"? → Use "id", "identifier", or "code"  
3. Does your field name match any protected word? → Choose alternative

**COMMON MISTAKES TO AVOID:**

```json
// WRONG - ALL these will FAIL:
"Person": {"fields": {"name": "str", "role": "str"}}        // ERROR: 'name'
"Team": {"fields": {"name": "str", "size": "int"}}          // ERROR: 'name'
"Location": {"fields": {"name": "str", "address": "str"}}   // ERROR: 'name'
"Project": {"fields": {"uuid": "str", "status": "str"}}     // ERROR: 'uuid'

// CORRECT - Use these patterns instead:
"Person": {"fields": {"role": "str", "department": "str"}}  // Good: no 'name'
"Team": {"fields": {"team_size": "int", "department": "str"}} // Good: no 'name'
"Location": {"fields": {}}  // Good: inherits 'name', no redefinition
"Project": {"fields": {"project_id": "str", "status": "str"}} // Good: no 'uuid'
```

**WHY THIS MATTERS:**
- ALL entities automatically inherit `name` from base model
- Redefining protected attributes causes immediate failure
- The system provides these attributes - you cannot override them

### Custom Entities

- **Define domain-specific types:** Use structured fields with dict format (not JSON strings).
- **Always check protected attributes above** before defining any custom entity.

### During Your Work

- **Respect discovered preferences:** Align your work with any preferences you've found.
- **Follow procedures exactly:** If you find a procedure for your current task, follow it step by step.
- **Apply relevant facts:** Use factual information to inform your decisions and recommendations.
- **Stay consistent:** Maintain consistency with previously identified preferences, procedures, and facts.

### Custom Types Example (MCP Tool Format)

```json
{
  "name": "Employee Info",
  "episode_body": "John works for TechCorp engineering team as a software engineer",
  "source": "text",
  "custom_entity_types": {
    "Person": {
      "fields": {"role": "str", "department": "str"},
      "docstring": "Person information"
    },
    "Company": {
      "fields": {"industry": "str", "size": "str"},
      "docstring": "Company information"
    },
    "Team": {
      "fields": {"department": "str", "team_size": "int"},
      "docstring": "Team within a company - inherits 'name' automatically"
    }
  },
  "custom_edge_types": {
    "WORKS_FOR": {
      "fields": {},
      "docstring": "Employment relationship"
    },
    "BELONGS_TO_TEAM": {
      "fields": {},
      "docstring": "Team membership"
    }
  },
  "custom_edge_mappings": {
    "('Person', 'Company')": ["WORKS_FOR"],
    "('Person', 'Team')": ["BELONGS_TO_TEAM"]
  }
}
```

### Best Practices

- **Search before suggesting:** Always check if there's established knowledge before making recommendations.
- **Combine node and fact searches:** For complex tasks, search both nodes and facts to build a complete picture.
- **Use `center_node_uuid`:** When exploring related information, center your search around a specific node.
- **Prioritize specific matches:** More specific information takes precedence over general information.
- **Be proactive:** If you notice patterns in user behavior, consider storing them as preferences or procedures.

**Remember:** The knowledge graph is your memory. Use it consistently to provide personalized assistance that respects the user's established preferences, procedures, and factual context.