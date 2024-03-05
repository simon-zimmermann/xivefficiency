/** @jsxImportSource @emotion/react */


import { Fragment, useCallback, useContext } from "react"
import { EventLoopContext, StateContexts } from "/utils/context"
import { Event, getBackendURL, isTrue, set_val } from "/utils/state"
import { WifiOffIcon as LucideWifiOffIcon } from "lucide-react"
import { keyframes } from "@emotion/react"
import { Box as RadixThemesBox, Button as RadixThemesButton, Container as RadixThemesContainer, Dialog as RadixThemesDialog, Flex as RadixThemesFlex, Text as RadixThemesText, Theme as RadixThemesTheme } from "@radix-ui/themes"
import env from "/env.json"
import "@radix-ui/themes/styles.css"
import theme from "/utils/theme.js"
import { DebounceInput } from "react-debounce-input"
import { Input } from "@chakra-ui/react"
import NextHead from "next/head"



export function Fragment_e9a05c105aa9215aeba52aeec8fe2e76 () {
  const state = useContext(StateContexts.state)
  const [addEvents, connectErrors] = useContext(EventLoopContext);


  return (
    <Fragment>
  {isTrue(((!state.is_hydrated) || (connectErrors.length > 0))) ? (
  <Fragment>
  <LucideWifiOffIcon css={{"color": "crimson", "zIndex": 9999, "position": "fixed", "bottom": "30px", "right": "30px", "animation": `${pulse} 1s infinite`}} size={32}>
  {`wifi_off`}
</LucideWifiOffIcon>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  )
}

export function Fragment_ac0b06893fc1b15016f3e0532508036d () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);


  return (
    <Fragment>
  {isTrue(connectErrors.length >= 2) ? (
  <Fragment>
  <RadixThemesDialog.Root css={{"zIndex": 9999}} open={connectErrors.length >= 2}>
  <RadixThemesDialog.Content>
  <RadixThemesDialog.Title>
  {`Connection Error`}
</RadixThemesDialog.Title>
  <RadixThemesText as={`p`}>
  {`Cannot connect to server: `}
  {(connectErrors.length > 0) ? connectErrors[connectErrors.length - 1].message : ''}
  {`. Check if server is reachable at `}
  {getBackendURL(env.EVENT).href}
</RadixThemesText>
</RadixThemesDialog.Content>
</RadixThemesDialog.Root>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  )
}

export function Box_5d38c543464657b2e976f3c13c7e0ee9 () {
  const state__state = useContext(StateContexts.state__state)


  return (
    <RadixThemesBox>
  {state__state.chat_history.map((messages, index_ba04add9a46f955705ec4619e54ba4db) => (
  <RadixThemesBox css={{"marginTop": "1em", "marginBottom": "1em"}} key={index_ba04add9a46f955705ec4619e54ba4db}>
  <RadixThemesBox css={{"textAlign": "right"}}>
  <RadixThemesText as={`p`} css={{"padding": "1em", "borderRadius": "5px", "marginTop": "0.5em", "marginBottom": "0.5em", "boxShadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px", "maxWidth": "30em", "display": "inline-block", "marginLeft": "20%"}}>
  {messages.at(0)}
</RadixThemesText>
</RadixThemesBox>
  <RadixThemesBox css={{"textAlign": "left"}}>
  <RadixThemesText as={`p`} css={{"padding": "1em", "borderRadius": "5px", "marginTop": "0.5em", "marginBottom": "0.5em", "boxShadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px", "maxWidth": "30em", "display": "inline-block", "marginRight": "20%"}}>
  {messages.at(1)}
</RadixThemesText>
</RadixThemesBox>
</RadixThemesBox>
))}
</RadixThemesBox>
  )
}

const pulse = keyframes`
    0% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
`


export function Button_99a5cd492a40f92cd4e437cbe2852d8d () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  const on_click_f4ecaeca7ac4803e870637fe18cb1eea = useCallback((_e) => addEvents([Event("state.state.answer", {})], (_e), {}), [addEvents, Event])

  return (
    <RadixThemesButton css={{"backgroundColor": "#CEFFEE", "boxShadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px"}} onClick={on_click_f4ecaeca7ac4803e870637fe18cb1eea}>
  {`Ask`}
</RadixThemesButton>
  )
}

export function Debounceinput_dce3472e8c5442c55f0ff4ef86c1dbae () {
  const state__state = useContext(StateContexts.state__state)
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  const on_change_c1fe93b939c866e1de40fb642568d5e0 = useCallback((_e0) => addEvents([Event("state.state.set_question", {value:_e0.target.value})], (_e0), {}), [addEvents, Event])

  return (
    <DebounceInput debounceTimeout={300} element={Input} onChange={on_change_c1fe93b939c866e1de40fb642568d5e0} placeholder={`Ask a question`} sx={{"borderWidth": "1px", "padding": "1em", "boxShadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px"}} value={state__state.question}/>
  )
}

export default function Component() {

  return (
    <Fragment>
  <Fragment>
  <div css={{"position": "fixed", "width": "100vw", "height": "0"}}>
  <Fragment_e9a05c105aa9215aeba52aeec8fe2e76/>
</div>
  <Fragment_ac0b06893fc1b15016f3e0532508036d/>
</Fragment>
  <RadixThemesContainer>
  <Box_5d38c543464657b2e976f3c13c7e0ee9/>
  <RadixThemesFlex align={`start`} direction={`row`} gap={`2`}>
  <Debounceinput_dce3472e8c5442c55f0ff4ef86c1dbae/>
  <Button_99a5cd492a40f92cd4e437cbe2852d8d/>
</RadixThemesFlex>
</RadixThemesContainer>
  <NextHead>
  <title>
  {`Reflex App`}
</title>
  <meta content={`A Reflex app.`} name={`description`}/>
  <meta content={`favicon.ico`} property={`og:image`}/>
</NextHead>
</Fragment>
  )
}
