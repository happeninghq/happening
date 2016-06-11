/**
 * This is a single-page application for editing
 * a "page" - adding/moving/editing/deleting
 * components.
 */
import reqwest from 'reqwest'
import _ from 'lodash'
import React from 'react'
import { render } from 'react-dom'
import { Provider, connect } from 'react-redux'
import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { DjangoCSRFToken } from './react/django'

const { PropTypes } = React;

export const init = () => {
	_.each(document.getElementsByClassName("edit-page"), (elem) => {

    // Initial configuration
    const blocktypes = JSON.parse(elem.dataset['blocktypes']);
    const valid_blocktypes = blocktypes.map(({type}) => type);
    const UnfilteredContent = JSON.parse(elem.dataset['content']);

    const getBlock = (blocks, id) => blocks.filter((b) => b.id == id)[0];

    const content = {
      blocks: UnfilteredContent.blocks.filter(
        (block) => valid_blocktypes.indexOf(block.type) > -1
      ),
      blockLists: UnfilteredContent.blockLists.map((l) => 
        l.filter((blockId) => valid_blocktypes.indexOf(getBlock(UnfilteredContent.blocks, blockId).type) > -1)
      ),
    };

		// ACTIONS

		const ADD_BLOCK = 'ADD_BLOCK';
		const DELETE_BLOCK = 'DELETE_BLOCK';
    const CHANGE_BLOCK_TYPE = 'CHANGE_BLOCK_TYPE';
    const EDIT_BLOCK = 'EDIT_BLOCK';
    const PREVIEW_BLOCK = 'PREVIEW_BLOCK';
    const RENDER = 'RENDER';
    const SET_FORM_VALUE = 'SET_FORM_VALUE';
    const INIT_UI = 'INIT_UI';


    // MODES

    const SELECT_TYPE = 'SELECT_TYPE';
    const EDIT = 'EDIT';
    const PREVIEW = 'PREVIEW';


		// ACTION CREATORS

		const AddBlock = (location) => {
      let id = 0;
      if (store.getState().blocks.length > 0) {
        id = _.max(store.getState().blocks.map((b) => b.id)) + 1;
      }
			return {
				type: ADD_BLOCK,
				id: id,
				location
			}
		}

    const InitUI = (block) => {
      return dispatch => {
        reqwest({
          url: "/staff/pages/block",
          data: block,
          type: "json"
        }).then(resp => {
          dispatch({
            type: RENDER,
            html: resp.html,
            id: block.id
          });
        })

        dispatch({
          type: INIT_UI,
          id: block.id
        });
      }
    }

		const DeleteBlock = (id) => {
			return {
				type: DELETE_BLOCK,
				id
			}
		}

    const StartEditBlock = (id) => {
      return {
        type: EDIT_BLOCK,
        id
      }
    }

    const SetFormValue = (id, fieldName, value) => {
      return {
        type: SET_FORM_VALUE,
        id,
        fieldName,
        value
      }
    }

    const StartPreviewBlock = (block) => {
      return dispatch => {
        reqwest({
          url: "/staff/pages/block",
          data: block,
          type: "json"
        }).then(resp => {
          dispatch({
            type: RENDER,
            html: resp.html,
            id: block.id
          });
        })

        dispatch({
          type: PREVIEW_BLOCK,
          id: block.id
        });
      }
    }

    const ChangeBlockType = (id, blockType) => {
      return {
        type: CHANGE_BLOCK_TYPE,
        id,
        blockType
      }
    }

		// Presentation

		const SelectTypeBlock = ({ block, blockTypes, onSelectBlockType }) => (
			<div>
        <ul>
          {blockTypes.map((i) =>
            <li key={i.type} onClick={e => onSelectBlockType(block.id, i.type)}>
              {i.type}
            </li>)}
        </ul>
      </div>
		)
    SelectTypeBlock.propTypes = {
      block: PropTypes.object.isRequired
    }


    const InputField = ({ field, value, onFieldChange }) => {
      let input;

      return <div className="form__field">
        <div className="form__field__label">
          <label>{field.name}</label>
        </div>
        <input defaultValue={value} type="text" ref={node => {
          input = node
        }} onKeyUp={e => onFieldChange(input.value)}></input>
      </div>
    }

    const EditBlock = ({ block, blockType, onFieldChange }) => {

      const formelements = blockType.fields.map((f) => (
        <InputField key={f.name} field={f} value={block[f.name]} onFieldChange={(value) =>
          onFieldChange(f.name, value)
        }></InputField>
      ));

      return <div>
        {formelements}
      </div>
    }

    const PreviewBlock = ({ block, blockUI }) => {
      if ( blockUI.renderedHTML != null) {
        return <div dangerouslySetInnerHTML={{__html: blockUI.renderedHTML}}></div>
      }

      return <div>
        Loading...
      </div>
    }

		const Block = ({ block, onDelete, onEdit, onPreview, mode }) => {

      let content = null;
      let extraLink = null
      if (mode == SELECT_TYPE) {
        content = <SelectTypeBlockContainer block={block}></SelectTypeBlockContainer>

        extraLink = <div>
          <a className="block__header-extra-link" href="#">
            <i className="fa fa-trash" title="Delete" onClick={e => {
              e.preventDefault()
              onDelete()
            }}></i>
          </a>
        </div>

      } else if (mode == EDIT) {
        content = <EditBlockContainer block={block}></EditBlockContainer>

        extraLink = <div>
          <a className="block__header-extra-link" href="#">
            <i className="fa fa-trash" title="Delete" onClick={e => {
              e.preventDefault()
              onDelete()
            }}></i>
          </a>
          <a className="block__header-extra-link" href="#">
            <i className="fa fa-play" title="Delete" onClick={e => {
              e.preventDefault()
              onPreview()
            }}></i>
          </a>
        </div>
      } else {
        content = <PreviewBlockContainer block={block}></PreviewBlockContainer>

        extraLink = <div>
          <a className="block__header-extra-link" href="#">
            <i className="fa fa-trash" title="Delete" onClick={e => {
              e.preventDefault()
              onDelete()
            }}></i>
          </a>
          <a className="block__header-extra-link" href="#">
            <i className="fa fa-pause" title="Delete" onClick={e => {
              e.preventDefault()
              onEdit()
            }}></i>
          </a>
        </div>
      }

      return (
			<div className="block block-list__item">
				<header className="block__header valign-together">
          <h2 className="block__header-text block__header-text--small">{block.title}</h2>

          { extraLink }

        </header>

        {content}
			</div>
		)}
    Block.propTypes = {
      block: PropTypes.shape({
      }).isRequired,
      onDelete: PropTypes.func.isRequired
    }

		const BlockList = ({ list, className, onAddBlock, additionalBlock }) => (
			<div className={className}>
				{list.map(i =>
					<BlockContainer key={i.id} block={i} />
				)}
				<div className="block block-list__item">
	  			<a href="#" onClick={e => {
            e.preventDefault()
            onAddBlock()
          }}>Add Block</a>
	  		</div>

        { additionalBlock }
			</div>
		)
    BlockList.propTypes = {
      list: PropTypes.arrayOf(PropTypes.shape({
      }).isRequired).isRequired,
      className: PropTypes.string.isRequired,
      onAddBlock: PropTypes.func.isRequired
    }

    const EditPage = ( { blockLists, onAddBlock, value } ) => {

      const submitBlock = <div className="block-list__item block">
        <header className="block__header valign-together">
          <h2 className="block__header-text block__header-text--small">Edit Page</h2>
        </header>
        <input type="hidden" name="content" value={value}></input>
        <button type="submit">Save</button>
      </div>

      return <form method="POST">
        <DjangoCSRFToken />
        <BlockList list={blockLists[0]} className="l-primary-content block-list" onAddBlock={() =>
          onAddBlock(0)
          } />
        <BlockList list={blockLists[1]} className="l-secondary-content block-list" additionalBlock={submitBlock} onAddBlock={() =>
          onAddBlock(1)
        } />
      </form>}

		// Container

    const App = connect(
      (state) => ({
        blockLists: state.blockLists.map((l) =>
          l.map((id) => state.blocks.filter((i) => i.id == id)[0])),
          value: JSON.stringify({blocks: state.blocks, blockLists: state.blockLists})
      }),
      (dispatch) => ({
        onAddBlock: (location) => {
          dispatch(AddBlock(location))
        }
      }))(EditPage)

    const SelectTypeBlockContainer = connect(
      (state) => ({
        blockTypes: state.blockTypes
      }),
      (dispatch) => ({
        onSelectBlockType: (id, type) => {
          dispatch(ChangeBlockType(id, type))
        }
      }))(SelectTypeBlock)

    const EditBlockContainer = connect(
      (state, { block }) => {
        return {
          blockType: state.blockTypes.filter((i) => i.type == block.type)[0]
      }},
      (dispatch, { block }) => ({
        onFieldChange: (fieldName, value) => {
          dispatch(SetFormValue(block.id, fieldName, value));
        }
      }))(EditBlock)

    const PreviewBlockContainer = connect(
      (state, { block }) => ({
        blockUI: state.blockUIs.filter((i) => i.id == block.id)[0]
      }),
      (dispatch) => ({
        
      }))(PreviewBlock)

    const BlockContainer = connect(
      (state, { block }) => ({
        mode: state.blockUIs.filter((b) => b.id == block.id)[0].mode
      }),
      (dispatch, { block }) => ({
        onDelete: () => {
          dispatch(DeleteBlock(block.id))
        },
        onEdit: () => {
          dispatch(StartEditBlock(block.id))
        },
        onPreview: () => {
          dispatch(StartPreviewBlock(block))
        },
        onSelectBlockType: (id, type) => {
          dispatch(ChangeBlockType(id, type))
        }
      }))(Block)

    // Reducers

		const block = (state, action) => {
			switch (action.type) {
				case ADD_BLOCK:
		  	  return {
            id: action.id,
            type: null
          };
        case CHANGE_BLOCK_TYPE:
          if (state.id == action.id) {
            return Object.assign({}, state, {type: action.blockType});
          }
          return state;
        case SET_FORM_VALUE:
          if (state.id == action.id) {
            let x = {}
            x[action.fieldName] = action.value;
            return Object.assign({}, state, x);
          }
          return state;
		  	default:
		      return state
			  }
		};

    const blocks = (state = content.blocks, action) => {
      switch (action.type) {
        case ADD_BLOCK:
          return [...state, block(undefined, action)];
        case DELETE_BLOCK:
          return state.filter((b) => b.id != action.id);
        case CHANGE_BLOCK_TYPE:
          return state.map((l) => block(l, action));
        case SET_FORM_VALUE:
          return state.map((l) => block(l, action));
        default:
          return state;
      }
    }

    const blockUI = (state, action) => {
      switch (action.type) {
        case ADD_BLOCK:
          return {
            id: action.id,
            mode: SELECT_TYPE,
            renderedHTML: null
          };
        case INIT_UI:
          return {
            id: action.id,
            mode: PREVIEW,
            renderedHTML: null
          };
        case CHANGE_BLOCK_TYPE:
          if (state.id == action.id && state.mode == SELECT_TYPE) {
            return Object.assign({}, state, {mode: EDIT});
          }
          return state;
        case EDIT_BLOCK:
          if (state.id == action.id) {
            return Object.assign({}, state, {mode: EDIT});
          }
          return state;
        case PREVIEW_BLOCK:
          if (state.id == action.id) {
            return Object.assign({}, state, {mode: PREVIEW, renderedHTML: null});
          }
          return state;
        case RENDER:
          if (state.id == action.id) {
            return Object.assign({}, state, {renderedHTML: action.html});
          }
          return state;
        default:
          return state
        }
    };

    const blockUIs = (state = [], action) => {
      switch (action.type) {
        case ADD_BLOCK:
        case INIT_UI:
          return [...state, blockUI(undefined, action)];
        case DELETE_BLOCK:
          return state.filter((b) => b.id != action.id);
        case CHANGE_BLOCK_TYPE:
          return state.map((l) => blockUI(l, action));
        case EDIT_BLOCK:
          return state.map((l) => blockUI(l, action));
        case PREVIEW_BLOCK:
          return state.map((l) => blockUI(l, action));
        case RENDER:
          return state.map((l) => blockUI(l, action));
        default:
          return state;
      }
    }

		const blockLists = (state = content.blockLists, action) => {
		  switch (action.type) {
  			case ADD_BLOCK:
  	  	  return state.map((l, i) => {
            if (i == action.location) {
  	  	  		return [...l, action.id];
  	  	  	}
  	  	  	return l;
  	  	  });
        case DELETE_BLOCK:
          return state.map((l) => l.filter((b) => b != action.id));
  	    default:
  	      return state
		  }
		}

    const blockTypes = (state = blocktypes, action) => {
      switch (action.type) {
        default:
          return state;
      }
    }

    const editPage = combineReducers({
      blockLists,
      blockTypes,
      blocks,
      blockUIs
    });

    const store = createStore(editPage, applyMiddleware(thunk));


    // We need to initialise the UI
    _.each(content.blocks, (block) => {
      store.dispatch(InitUI(block));
    });

		render(
		  <Provider store={store}>
		    <App />
		  </Provider>,
		  elem
		);
	});
}