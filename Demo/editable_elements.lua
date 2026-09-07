-- Export native elements through Quarto/Pandoc. build_editable.py positions
-- those elements and assembles the original 44 reveal slides.
local counts={1,1,1,1,1,1,1,1,1,1,4,1,1,3,1,3,3}
function Pandoc(doc)
  local output=pandoc.Blocks({})
  local manifest={}
  local title,body
  local frame,fragment=0,0
  local function emit()
    if not title then return end
    frame=frame+1
    local slots,notes={},pandoc.Blocks({})
    local counters={F=0,L=0,R=0}
    local last
    local function append(block,zone,start)
      local kind='text'
      if block.t=='Table' then kind='table'
      elseif block.t=='Para' and #block.content==1 and block.content[1].t=='Image' then kind='image' end
      if kind~='text' or not last or last.zone~=zone or last.kind~='text' then
        last={zone=zone,key=zone..counters[zone],kind=kind,blocks={}}
        counters[zone]=counters[zone]+1
        slots[#slots+1]=last
      end
      last.blocks[#last.blocks+1]={block=block,start=start}
    end
    local collect
    collect=function(blocks,zone,start)
      for _,b in ipairs(blocks) do
        if b.t=='Div' then
          if b.classes:includes('notes') then notes:insert(b)
          elseif b.classes:includes('columns') then
            last=nil
            for i,col in ipairs(b.content) do
              collect(col.content,i==1 and 'L' or 'R',start)
              last=nil
            end
          else collect(b.content,zone,math.max(start,tonumber(b.attributes['from'] or '1'))) end
        else append(b,zone,start) end
      end
    end
    collect(body,'F',1)
    for step=1,tonumber(title.attributes.steps or '1') do
      local record={frame=frame,step=step,elements={}}
      fragment=fragment+1; record.title=fragment
      output:insert(pandoc.Header(2,title.content,pandoc.Attr('title-'..fragment)))
      output:extend(notes)
      for _,slot in ipairs(slots) do
        local visible=pandoc.Blocks({})
        for _,entry in ipairs(slot.blocks) do
          if step>=entry.start then visible:insert(entry.block) end
        end
        if #visible>0 then
          visible=pandoc.Pandoc(visible):walk({Image=function(img)
            local id=tonumber(img.attributes.diagram)
            if id then
              local phase=math.min(counts[id],step)
              img.src=string.format('editable_assets/diagram-%02d-%d.png',id,phase)
              img.attributes.diagram=nil
              img.attributes['phase-start']=nil
            end
            return img
          end}).blocks
          fragment=fragment+1
          output:insert(pandoc.Header(2,'Element '..fragment))
          output:extend(visible)
          record.elements[#record.elements+1]={fragment=fragment,key=slot.key,kind=slot.kind}
        end
      end
      manifest[#manifest+1]=record
    end
  end
  for _,b in ipairs(doc.blocks) do
    if b.t=='Header' and b.level==2 then emit();title=b;body=pandoc.Blocks({})
    elseif title then body:insert(b) end
  end
  emit()
  local f=assert(io.open('build/editable/elements.json','w'))
  f:write(pandoc.json.encode({slides=manifest,fragments=fragment}));f:close()
  return pandoc.Pandoc(output,doc.meta)
end
