import {babel} from '@rollup/plugin-babel';
import commonjs from '@rollup/plugin-commonjs';
import {terser} from "rollup-plugin-terser";
import {nodeResolve} from '@rollup/plugin-node-resolve';

export default [{
  input: ['-'],
  plugins: [
    nodeResolve({browser: true}),
    commonjs(),
    babel({
      babelHelpers: 'inline',
      presets: [
        [require('@babel/preset-env'),
          {targets: ["ios >= 5", "android >= 4"]}]
      ]
    }),
    terser({
      mangle: {
        // Prevent mangling of one-character functions
        keep_fnames: /./,
      },
      format: {
        // Necessary for generating Anki play buttons
        comments: /EOL\s*{{.*?}}\s*EOL/
      }
    })
  ]
}];