"use client";
import { useEffect, useRef } from "react";
import JsBarcode from "jsbarcode";
import DemoFingerprint from "./demo-fingerprint";

export default function DemoBarcode({ reference }) {
	const svg = useRef(null);
	useEffect(() => {
		JsBarcode(svg.current, reference, {
			format: "CODE128",
			displayValue: true,
			fontSize: 13,
			width: 2,
			height: 60,
			margin: 16,
		});
	}, [reference]);
	return (
		<figure className="demo-barcode">
			<DemoFingerprint phase="complete" />
			<figcaption>
				<strong>SIMULATED CAPTURE — DEMO ONLY</strong>
				<p>Random barcode reference; not a fingerprint or attendance credential.</p>
			</figcaption>
			<svg ref={svg} role="img" aria-label={`Demo barcode ${reference}`} />
			<code>{reference}</code>
		</figure>
	);
}
